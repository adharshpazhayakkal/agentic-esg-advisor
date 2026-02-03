from rank_bm25 import BM25Okapi
import re

def chunk_text(text, chunk_size=120):
    words = re.findall(r"\w+", text.lower())
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = words[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

def retrieve_relevant_chunks(text, queries, top_k=3):
    chunks = chunk_text(text)
    if not chunks:
        return []

    bm25 = BM25Okapi(chunks)

    retrieved = []
    for q in queries:
        tokenized_q = q.lower().split()
        scores = bm25.get_scores(tokenized_q)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        for idx in top_indices:
            retrieved.append(" ".join(chunks[idx]))

    # Deduplicate
    return list(set(retrieved))
