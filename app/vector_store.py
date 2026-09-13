import chromadb


client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)


def store_embeddings(
    chunks,
    embeddings,
    document_id,
    user_id
):
    ids = []
    metadatas = []

    for index in range(len(chunks)):
        ids.append(
            f"document_{document_id}_chunk_{index}"
        )

        metadatas.append({
            "document_id": document_id,
            "user_id": user_id,
            "chunk_index": index
        })

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )


    '''ID
document_7_chunk_1

Embedding
[0.023, -0.081, 0.044, ...]

Document
"FastAPI uses dependency injection..."

Metadata
{
    "document_id": 7,
    "user_id": 3,
    "chunk_index": 1
}'''