import chromadb
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from typer import prompt

# local embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# local generation model — small, runs on CPU
generator = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_collection("banking_policies")

SYSTEM_PROMPT = """You are a banking compliance assistant. Answer questions 
about KYC/AML procedures and regulatory guidance using ONLY the provided 
context. If the context doesn't contain the answer, say so explicitly. 
Be precise and cite the source document AT ALL TIMES using [Source: filename]."""

def retrieve(query: str, top_k=4) -> list[dict]:
    embedding = embed_model.encode([query]).tolist()
    results = collection.query(query_embeddings=embedding, n_results=top_k)
    return [
        {"text": doc, "source": meta["source"]}
        for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    ]

def answer(query: str) -> dict:
    chunks = retrieve(query)
    context = "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    )
    prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
    
    response = generator(prompt, max_new_tokens=300, truncation=True)
    answer_text = response[0]["generated_text"]

    return {
        "query": query,
        "answer": answer_text,
        "retrieved_chunks": chunks,
        "model": "flan-t5-base",
    }

if __name__ == "__main__":
    result = answer("What documents are required for KYC verification?")
    print(result["answer"])