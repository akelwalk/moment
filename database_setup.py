from database_manager import DatabaseManager
from embeddings import Embeddings

dbm = DatabaseManager("moment.db")
embeddings = Embeddings()
dbm.open()

# creating journal entries table scheme
entriesTable = """CREATE TABLE IF NOT EXISTS
entries(entry_id INTEGER PRIMARY KEY AUTOINCREMENT, prompt TEXT, title TEXT, content TEXT, date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP, sentiment TEXT)"""

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
        "sentiment": None,
        "content_embedding": None
    },
    {
        "prompt": "How did you feel when you woke up?",
        "title": "Morning Thoughts",
        "content": "I woke up feeling anxious about the day ahead. The mounting tasks made me uneasy, and I had trouble focusing even on simple things.",
        "date_posted": "2025-08-29 07:45:00",
        "sentiment": None,
        "content_embedding": None
    },
    {
        "prompt": "Describe a recent situation that made you happy",
        "title": "Joyful Surprise",
        "content": "A friend sent me a heartfelt message today. It made me feel appreciated and valued. I realized how lucky I am to have such thoughtful people in my life.",
        "date_posted": "2025-08-31 14:30:00",
        "sentiment": None,
        "content_embedding": None
    },
    {
        "prompt": "What are you grateful for today?",
        "title": "Gratitude List",
        "content": "I felt a wave of love when I saw my family enjoying dinner together. Their laughter and warmth reminded me of the deep connections I cherish.",
        "date_posted": "2025-09-01 08:20:00",
        "sentiment": None,
        "content_embedding": None
    },
    {
        "prompt": "Describe your ideal day",
        "title": "Perfect Day",
        "content": "I imagined a day with endless traffic jams and missed meetings. The thought made me tense and frustrated, realizing how much I rely on things going smoothly.",
        "date_posted": "2025-09-02 10:05:00",
        "sentiment": None,
        "content_embedding": None
    },
    {
        "prompt": "How do you react to stress?",
        "title": "Stressful Moments",
        "content": "I felt scared today when I got an urgent message from work while traveling. My heart raced and I struggled to calm myself before responding.",
        "date_posted": "2025-09-02 12:45:00",
        "sentiment": None,
        "content_embedding": None
    },
    {
        "prompt": "What are your top three values in life?",
        "title": "Core Values",
        "content": "I was surprised today when a colleague praised a choice I made that I thought was minor. It made me rethink how my actions are perceived.",
        "date_posted": "2025-09-02 15:30:00",
        "sentiment": None,
        "content_embedding": None
    },
    {
        "prompt": "Describe a recent situation that made you happy",
        "title": "Small Joys",
        "content": "I felt pure joy when I saw my favorite band perform live, a moment I had been waiting for months. The energy in the crowd was contagious.",
        "date_posted": "2025-09-02 18:10:00",
        "sentiment": None,
        "content_embedding": None
    },
    {
        "prompt": "What fears are holding you back?",
        "title": "Facing Fears",
        "content": "I realized I have been avoiding asking for help at work due to fear of judgment. Acknowledging this fear is the first step to overcoming it. I plan to reach out to a mentor tomorrow.",
        "date_posted": "2025-09-03 09:50:00",
        "sentiment": None,
        "content_embedding": None
    },
    {
        "prompt": "Describe a recent situation that made you happy",
        "title": "Unexpected Happiness",
        "content": "I found an old notebook full of sketches from college. Looking through it brought back fond memories. I laughed at some of my early attempts and felt nostalgic.",
        "date_posted": "2025-09-03 17:20:00",
        "sentiment": None,
        "content_embedding": None
    }
]

# insert each entry into the database
for entry in entries:
    content = entry["content"]
    sentiment = embeddings.get_emotions(content) # returns a single emotion as a str
    content_embedding = embeddings.get_vector_embedding(content) # returns a binary blob
    dbm.insert(prompt=entry["prompt"], title=entry["title"], content=content, date_posted=entry["date_posted"], sentiment=sentiment, content_embedding=content_embedding)


dbm.close()