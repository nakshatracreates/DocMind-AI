from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas import usercreate,userlogin,questionrequest
from app.auth import hash_password,verify_password,create_token,get_current_user
from app.database import get_db
from app.models import users,documents
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi import FastAPI,UploadFile,File
from pypdf import PdfReader
from app.embedding import create_embeddings
from app.vector_store import store_embeddings
from app.chunking import chunk_text
from app.retriever import get_relevant_chunks
from app.context_builder import build_context
from app.genrator import generate_answer
from dotenv import load_dotenv
import  os

load_dotenv()
app=FastAPI()
apikey=os.getenv("OPENAI_API_KEY")


@app.get("/")
def home():
    return {"message": "DocMind API is running"}

@app.post("/register")
def register(user:usercreate,db:Session=Depends(get_db)):
    existing_user=db.execute(select(users).where(users.email==user.email)).scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    hashed_password=hash_password(user.password)
    new_user=users(
        email=user.email,
        password_hash=hashed_password
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Registration Failed"
        )
    return{
        "email":new_user.email,
        "message":"registration request received"
    }

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.execute(
        select(users).where(users.email == form_data.username)
    ).scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_token(
        {"sub": str(existing_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
@app.get("/profile")
def profile(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }

@app.post("/documents/upload")
def upload_document(
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
        status_code=400,
        detail="Only PDF files are allowed"
    )
    # Save PDF
    file_path = f"uploads/{file.filename}"

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
    except Exception:
        raise HTTPException(
        status_code=500,
        detail="Failed to save file"
    )

    # Create document record in PostgreSQL
    new_document = documents(
        filename=file.filename,
        file_path=file_path,
        user_id=current_user.id
    )
    try:
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
    except Exception:
        db.rollback()
        raise HTTPException(
        status_code=500,
        detail="Failed to save document information"
    )

    # Extract text from PDF
    try:
        reader = PdfReader(file_path)

        document_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                document_text += text

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read PDF file"
        )

    # Create chunks
    chunks = chunk_text(
        document_text,
        chunk_size=1000,
        overlap=200
    )

    # Create embeddings
    try:
        embeddings = create_embeddings(chunks)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to create embeddings"
        )
    # Store chunks + embeddings in ChromaDB
    try:
        store_embeddings(
            chunks=chunks,
            embeddings=embeddings,
            document_id=new_document.id,
            user_id=current_user.id
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to store document embeddings"
        )
    return {
        "id": new_document.id,
        "filename": new_document.filename,
        "user_id": new_document.user_id,
        "chunks": len(chunks),
        "message": "File uploaded and processed successfully"
    }


@app.get("/documents")
def get_documents(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    result=db.execute(select(documents).where(documents.user_id==current_user.id))
    document_list=result.scalars().all()
    return document_list

@app.post("/documents/ask")
def ask_document(request:questionrequest,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        chunks=get_relevant_chunks(question=request.question,user_id=current_user.id,db=db)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve relevant document content"
        )

    context=build_context(chunks)

    try:
        answer=generate_answer(question=request.question,context=context)
    except Exception:
        raise HTTPException(
        status_code=500,
        detail="Failed to generate answer"
    )
    return{"question":request.question,
           "answer":answer,
            "Sources":chunks
           }
