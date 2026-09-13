
def chunk_text(text,chunk_size,overlap):
    paragraphs=text.strip().split("\n\n")
    chunks=[]
    current_chunk=""

    for paragraph in paragraphs:
        if len(paragraph)>chunk_size:
            start=0

            while start<len(paragraph):
                end=start+chunk_size
                chunks.append(paragraph[start:end])

                start=end-overlap
        elif len(current_chunk)+len(paragraph)<=chunk_size:
            current_chunk+=paragraph+"\n\n"
        else:
            chunks.append(current_chunk)

            current_chunk = (
            current_chunk[-overlap:]
            + paragraph
            + "\n\n"
        )

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


'''Take processed chunks + their embeddings → store them in ChromaDB.'''