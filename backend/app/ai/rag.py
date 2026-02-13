from backend.app.ai.vector_store import model, index, texts

def retrieve_context(query: str, k: int = 3):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k)

    results = []
    for i, distance in zip(indices[0], distances[0]):
        if distance < 1.2:  # threshold tuning
            results.append(texts[i])

    return "\n\n".join(results)


