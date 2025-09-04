from fastapi import FastAPI, Body, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from database_manager import DatabaseManager
from embeddings import Embeddings
from journal_prompt_agent import JournalPromptAgent
import json5

# objects
dbm = DatabaseManager("moment.db")
embeddings = Embeddings()
model = ChatOllama(model="phi4-mini", temperature=1)
journal_prompt_agent = JournalPromptAgent(model, tools=[])

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static") # serving all the html/css/javascript pages in the static folder

class Entry(BaseModel):
    prompt: str
    title: str
    content: str

class UpdatedEntry(BaseModel):
    entry_id: int
    prompt: str
    title: str
    content: str
    sentiment: str

class SearchQuery(BaseModel):
    query: str

class Prompt(BaseModel):
    entry: str

# saving new entry to database
@app.post("/save_entry")
def create_entry(entry: Entry):
    e = entry.model_dump()
    content = e["content"]
    sentiment = embeddings.get_emotions(content) # returns a single emotion as a str
    content_embedding = embeddings.get_vector_embedding(content) # returns a binary blob
    dbm.open()
    dbm.insert(prompt=e["prompt"], title=e["title"], content=content, sentiment=sentiment.lower(), content_embedding=content_embedding)
    dbm.close()
    return {"status": 200, "received": e}

# getting all the entries
@app.get("/display_entries")
def display_entries():
    query = """SELECT entry_id, title, prompt, content, sentiment, date_posted FROM entries"""
    dbm.open()
    result = dbm.run_query(query)
    dbm.close()
    entries = [dict(r) for r in result]
    return {"status": 200, "entries": entries}

# update/get/delete a specific entry
@app.put("/entries/{entry_id}")
def update_entry(entry_id: int, entry: UpdatedEntry):
    e = entry.model_dump()
    content = e["content"]
    content_embedding = embeddings.get_vector_embedding(content)
    dbm.open()
    dbm.update(entry_id, e["title"], e["prompt"], content, e["sentiment"].lower(), content_embedding)
    dbm.close()
    return {"status": 200, "updated": e}

@app.get("/entries/{entry_id}")
def get_entry(entry_id: int):
    dbm.open()
    try:
        result = dbm.run_query("""SELECT * FROM entries WHERE entry_id = ?""", (entry_id,))[0]
    except:
        raise HTTPException(status_code=404, detail=f"Entry {entry_id} not found")
    dbm.close()
    entry = dict(result)
    return {"status": 200, "entry": entry} 

@app.delete("/entries/{entry_id}")
def delete_entry(entry_id: int):
    dbm.open()
    dbm.delete(entry_id) #TODO: raise http except if resource not found
    dbm.close()
    return {"status": 200, "deleted": entry_id}

@app.post("/search")
def search(search_query: SearchQuery):
    sq = search_query.model_dump()["query"]
    dbm.open()
    sq_embedding = embeddings.get_vector_embedding(sq)
    query = """SELECT e.entry_id, title, prompt, content, sentiment, date_posted, vec_distance_cosine(content_embedding, ?) AS score FROM embeddings emb JOIN entries e ON emb.entry_id = e.entry_id ORDER BY score ASC LIMIT 10"""
    result = dbm.cursor.execute(query, (sq_embedding,)).fetchall()
    dbm.close()
    entries = [dict(r) for r in result]
    return {"status": 200, "entries": entries}

@app.post("/generate_prompt")
def generate_prompt(entry: Prompt):
    e = json5.dumps(entry.model_dump())
    print(e)
    journal_prompt_agent.run(e)
    result = journal_prompt_agent.last_message
    print(result)
    r_dictionary = json5.loads(result)
    return {"status": 200, "prompt": r_dictionary["prompt"]}

#i hard coded the values in the graph - so api for getting counts per day? - adding emotions of entries to the same bar graph? - need a legend
#different graph for emotions per entry and their 
