from db import db_connect
from task_log import start_task, end_task


start_task("Importing sentence_transformers")

from sentence_transformers import SentenceTransformer, util

end_task()

sentences = [
    "No amount of evidence will ever persuade an idiot.",
    "Politicians and diapers must be changed often, and for the same reason.",
    "Most of the things I worried about in life never happened.",
    "Life is short, Break the Rules. Forgive quickly, Kiss slowly. Love truly. Laugh uncontrollably And never regret ANYTHING That makes you smile.",
    "I was educated once - it took me years to get over it.",
    "Kindness is the language which the deaf can hear and the blind can see.",
    "Never argue with stupid people, they will drag you down to their level and then beat you with experience.",
    "Why waste your money looking up your family tree? Just go into politics and your opponent will do it for you.",
    "Good decisions come from experience. Experience comes from making bad decisions.",
    "Give every day the chance to become the most beautiful day of your life.",
    "If you don't read the newspaper, you're uninformed. If you read the newspaper, you're mis-informed.",
    "Continuous improvement is better than delayed perfection."
    "The two most important days in your life are the day you are born and the day you find out why.",
    "Never put off till tomorrow what you can do the day after tomorrow.",
    "When I was 17, my father was so stupid, I didn't want to be seen with him in public. When I was 24, I was amazed at how much the old man had learned in just 7 years.",
    "How easy it is to make people believe a lie, and [how] hard it is to undo that work again!",
    "Do not complain about growing old. It is a privilege denied to many.",
    "Temper is what gets most of us into trouble. Pride is what keeps us there.",
    "If ignorance is bliss, why isn't the world happier?",
    "To be great, truly great, you have to be the kind of person who makes the others around you great.",
    "Some people bring joy wherever they go, and some people bring joy whenever they go.",
    "If voting made any difference they wouldn't let us do it.",
    "The secret of getting ahead is getting started. The secret of getting started is breaking your complex overwhelming tasks into small manageable tasks, and starting on the first one."
    "Worrying is like paying a debt you don't owe.",
    "Never argue with a fool, onlookers may not be able to tell the difference.",
    "Whenever you find yourself on the side of the majority, it is time to pause and reflect.",
]

start_task("Loading model")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
end_task()

start_task("Computing embeddings")
embeddings = model.encode(sentences)
end_task()

dimensions = len(embeddings[0])


start_task("Inserting into database")

with db_connect() as conn:
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION vector;")
        cur.execute(
            f"""
                create table if not exists chunks (
                    id bigserial primary key,
                    embedding vector ({dimensions}),
                    text text
                );
            """
        )

        for sentence, embedding in zip(sentences, embeddings):
            cur.execute(
                "insert into chunks (embedding, text) values (%s, %s);",
                ([float(e) for e in embedding], sentence),
            )


end_task()
