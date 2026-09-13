import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import documents


load_dotenv()

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="documents"
)

openai_client = OpenAI()


def retrieve_chunks(question, user_id, n_results=3):

    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    question_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results,
        where={"user_id": user_id}
    )

    return results

def get_relevant_chunks(question, user_id, db: Session, n_results=3):

    results = retrieve_chunks(
        question,
        user_id,
        n_results
    )

    chunks = []

    retrieved_documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for index in range(len(retrieved_documents)):

        document = db.execute(
            select(documents).where(
                documents.id == metadatas[index]["document_id"]
            )
        ).scalar_one_or_none()

        chunks.append({
            "text": retrieved_documents[index],
            "document_id": document.id,
            "chunk_index": metadatas[index]["chunk_index"],
            "filename": document.filename
        })

    return chunks