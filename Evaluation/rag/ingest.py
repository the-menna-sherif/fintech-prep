import os
from pathlib import Path
from time import time
from dotenv import load_dotenv
import chromadb
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
from pypdf import PdfReader

CHUNK_SIZE = 500       # tokens approx
CHUNK_OVERLAP = 50

# fxn to load documents, checks file type then extracts text (pdf, md, etc.)
# returns list of dicts with source and text for each doc
def load_documents(corpus_dir: str) -> list[dict]:
    docs = []
    for path in Path(corpus_dir).iterdir():
        if path.suffix == ".pdf":
            reader = PdfReader(str(path))
            text = "\n".join(p.extract_text() for p in reader.pages)
        elif path.suffix in (".md", ".txt"):
            text = path.read_text()
        else:
            continue
        docs.append({"source": path.name, "text": text})
    return docs

# simple chunking fxn by splitting on whitespace
# returns list of text chunks for a given document
def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# main ingestion fxn to load docs, chunk, embed, and store in ChromaDB
# returns nothing but prints total chunks ingested at the end
def ingest(corpus_dir="corpus/"):
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection("banking_policies")

    docs = load_documents(corpus_dir)
    for doc in docs:
        chunks = chunk_text(doc["text"])
        
        # embed each chunk individually (Google API is per-call, not batched)
        embeddings = []
        for chunk in chunks:
            result = genai.embed_content(
                model="models/embedding-001",
                content=chunk,
                task_type="retrieval_document"
            )
            embeddings.append(result["embedding"])
            time.sleep(0.5)  # avoid rate limiting on free tier
        
        ids = [f"{doc['source']}_{i}" for i in range(len(chunks))]
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=[{"source": doc["source"]}] * len(chunks)
        )
    print(f"Ingested {sum(len(chunk_text(d['text'])) for d in docs)} chunks.")

if __name__ == "__main__":
    ingest()