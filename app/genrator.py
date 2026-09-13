from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()


def generate_answer(question, context):

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document question-answering assistant. "
                    "Answer the user's question using only the provided context. "
                    "If the answer is not present in the context, say "
                    "you could not find the answer in the documents."
                )
            },
            {
                "role": "user",
                "content": f"""
Context:

{context}

Question:

{question}
"""
            }
        ]
    )

    return response.choices[0].message.content