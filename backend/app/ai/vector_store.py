import faiss
from sentence_transformers import SentenceTransformer
from backend.app.knowledge_base.faqs import KNOWLEDGE_BASE

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    f"{item['category']} - {item['question']} - {item['answer']}"
    for item in KNOWLEDGE_BASE
]

embeddings = model.encode(texts)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)
