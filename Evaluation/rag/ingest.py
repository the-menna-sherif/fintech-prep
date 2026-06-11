import os
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
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
    model = SentenceTransformer("all-MiniLM-L6-v2") # embedding model for vector reps of text chunks
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("banking_policies")

    docs = load_documents(corpus_dir) # grab dicts of source and text for each doc in corpus from fxn
    for doc in docs:
        chunks = chunk_text(doc["text"]) # pass text to chunking fxn to get list of text chunks for each doc
        embeddings = model.encode(chunks).tolist() # get vector embeddings for each chunk using the sentence transformer model, convert to list for ChromaDB
        ids = [f"{doc['source']}_{i}" for i in range(len(chunks))]
        # data saved for each source: chunk text, embedding vector, unique id, and metadata with source filename for traceability
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=[{"source": doc["source"]}] * len(chunks)
        )
    print(f"Ingested {sum(len(chunk_text(d['text'])) for d in docs)} chunks.")

if __name__ == "__main__":
    ingest()