from backend.app.knowledge_base.faqs import KNOWLEDGE_BASE

def generate_draft_reply(ticket_text: str):
    context = retrieve_context(ticket_text)

    return (
        "Based on our records:\n\n"
        f"{context}\n\n"
        "If you need further help, please let us know."
    )

from backend.app.ai.vector_store import model, index, texts

def retrieve_context(query: str):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k=1)

    return texts[indices[0][0]]
