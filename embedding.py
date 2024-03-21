from task_log import task


_cached_model = None


def load_embedding_model():
    global _cached_model
    if _cached_model is None:
        with task("Importing sentence_transformers"):
            from sentence_transformers import SentenceTransformer
        with task("Loading model"):
            _cached_model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )
    return _cached_model
