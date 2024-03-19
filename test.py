from task_log import start_task, end_task

start_task("Importing sentence_transformers")
from sentence_transformers import SentenceTransformer

end_task()

sentences = ["This is an example sentence", "Each sentence is converted"]

start_task("Loading model")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
end_task()

start_task("Computing embeddings")
embeddings = model.encode(sentences)
end_task()

print(embeddings)
