from database_manager import DatabaseManager
from embeddings import Embeddings

dbm = DatabaseManager("moment.db")
embedding = Embeddings()
dbm.open()

# creating journal entries table scheme
entriesTable = """CREATE TABLE IF NOT EXISTS
entries(entry_id INTEGER PRIMARY KEY AUTOINCREMENT, prompt TEXT, title TEXT, content TEXT, date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP, sentiments TEXT)"""

embeddingsTable = """CREATE VIRTUAL TABLE IF NOT EXISTS embeddings 
USING vec0(entry_id INTEGER PRIMARY KEY, content_embedding float[384])"""

dbm.run_query(entriesTable)
dbm.run_query(embeddingsTable)

entries = [
    {
        "prompt": "Reflect on a small win today",
        "title": "A Small Victory",
        "content": "Today I finally managed to fix that bug I had been stuck on for hours. It felt so satisfying to see my code run without errors. I celebrated with a cup of tea.",
        "date_posted": "2025-08-29 09:15:00",
        "sentiments": None,
        "content_embedding": None
    },
    {
        "prompt": "How did you feel when you woke up?",
        "title": "Morning Thoughts",
        "content": "I woke up feeling surprisingly energized despite staying up late. The sunlight streaming in my window lifted my mood. I decided to go for a short walk.",
        "date_posted": "2025-08-29 07:45:00",
        "sentiments": None,
        "content_embedding": None
    },
    {
        "prompt": "Describe a recent situation that made you happy",
        "title": "Joyful Surprise",
        "content": "A friend sent me a heartfelt message today. It made me feel appreciated and valued. I realized how lucky I am to have such thoughtful people in my life.",
        "date_posted": "2025-08-31 14:30:00",
        "sentiments": None,
        "content_embedding": None
    },
    {
        "prompt": "What are you grateful for today?",
        "title": "Gratitude List",
        "content": "I am grateful for the quiet morning coffee, the sunny weather, and my supportive colleagues. These little things really brighten my day. I want to make sure I notice them more often.",
        "date_posted": "2025-09-01 08:20:00",
        "sentiments": None,
        "content_embedding": None
    },
    {
        "prompt": "Describe your ideal day",
        "title": "Perfect Day",
        "content": "I imagined a day with no deadlines, a long hike in the mountains, and a good book by the evening. Everything felt calm and balanced in my mind. I wish I could make this happen more often.",
        "date_posted": "2025-09-02 10:05:00",
        "sentiments": None,
        "content_embedding": None
    },
    {
        "prompt": "How do you react to stress?",
        "title": "Stressful Moments",
        "content": "Today was overwhelming at work. I found myself pacing and taking deep breaths to calm down. Eventually, I managed to tackle the tasks one by one.",
        "date_posted": "2025-09-02 12:45:00",
        "sentiments": None,
        "content_embedding": None
    },
    {
        "prompt": "What are your top three values in life?",
        "title": "Core Values",
        "content": "I value honesty, curiosity, and empathy the most. They guide my decisions and interactions every day. Living by them makes me feel aligned and purposeful.",
        "date_posted": "2025-09-02 15:30:00",
        "sentiments": None,
        "content_embedding": None
    },
    {
        "prompt": "Describe a recent situation that made you happy",
        "title": "Small Joys",
        "content": "A stranger complimented my work today, which was unexpected but uplifting. It reminded me that small gestures can make a big difference. I ended the day with a smile.",
        "date_posted": "2025-09-02 18:10:00",
        "sentiments": None,
        "content_embedding": None
    },
    {
        "prompt": "What fears are holding you back?",
        "title": "Facing Fears",
        "content": "I realized I have been avoiding asking for help at work due to fear of judgment. Acknowledging this fear is the first step to overcoming it. I plan to reach out to a mentor tomorrow.",
        "date_posted": "2025-09-03 09:50:00",
        "sentiments": None,
        "content_embedding": None
    },
    {
        "prompt": "Describe a recent situation that made you happy",
        "title": "Unexpected Happiness",
        "content": "I found an old notebook full of sketches from college. Looking through it brought back fond memories. I laughed at some of my early attempts and felt nostalgic.",
        "date_posted": "2025-09-03 17:20:00",
        "sentiments": None,
        "content_embedding": None
    }
]

# insert each entry into the database
for entry in entries:
    content = entry["content"]
    sentiments = embedding.get_emotions(content) # returns a json string
    content_embedding = embedding.get_vector_embedding(content) # returns a binary blob

    dbm.cursor.execute(
        """INSERT INTO entries (prompt, title, content, date_posted, sentiments) VALUES (?, ?, ?, ?, ?)""",
        (entry["prompt"], entry["title"], content, entry["date_posted"], sentiments)
    )
    entry_id = dbm.cursor.lastrowid # getting the primary key of the row we just inserted
    dbm.cursor.execute(
        """INSERT INTO embeddings (entry_id, content_embedding) VALUES (?, ?)""",
        (entry_id, content_embedding)
    )

# test_query = """SELECT * FROM entries LIMIT 1 OFFSET 5"""
# result = dbm.run_query(test_query)[0]
# print(result["entry_id"])
# print(result["prompt"])
# print(result["title"])
# print(result["content"])
# print(result["sentiments"])

# testing out a embedding query thing
# query_embedding = embedding.get_vector_embedding("revisting through old moments")
# query = """SELECT entry_id, vec_distance_cosine(content_embedding, ?) AS score FROM embeddings ORDER BY score ASC LIMIT 5"""
# result = dbm.cursor.execute(query, (query_embedding,)).fetchall()
# print(result[0]["entry_id"])

dbm.close()