import faiss
import os
import numpy as np
from sentence_transformers import SentenceTransformer

KB_PATH = "backend/app/knowledge_base/faqs.txt"
INDEX_PATH = "backend/app/knowledge_base/faiss.index"
TEXTS_PATH = "backend/app/knowledge_base/texts.npy"

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_kb():
    with open(KB_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
    return chunks

if os.path.exists(INDEX_PATH) and os.path.exists(TEXTS_PATH):
    index = faiss.read_index(INDEX_PATH)
    texts = np.load(TEXTS_PATH, allow_pickle=True).tolist()
else:
    texts = load_kb()
    embeddings = model.encode(texts)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))

    faiss.write_index(index, INDEX_PATH)
    np.save(TEXTS_PATH, np.array(texts))
