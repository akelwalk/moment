import sqlite3
import sqlite_vec

class DatabaseManager():
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def open(self):
        # define connection
        self.connection = sqlite3.connect(self.db_name)
        self.connection.execute("PRAGMA foreign_keys = ON")  # need this after every connection

        self.connection.enable_load_extension(True)
        sqlite_vec.load(self.connection) # loading up the sqlite extention for vectors, need this after every connection
        self.connection.enable_load_extension(False)

        self.connection.row_factory = sqlite3.Row # now the output results of a list of row tuples will behave like dictionaries 
        self.cursor = self.connection.cursor()
    
    def close(self):
        self.connection.commit() # saving any modified data to the database
        self.connection.close()
    
    def insert(self, prompt, title, content, sentiment, content_embedding, date_posted): # date_posted is specified
        query = """INSERT INTO entries (prompt, title, content, date_posted, sentiment) VALUES (?, ?, ?, ?, ?)"""
        self.run_query(query=query, parameters=(prompt, title, content, date_posted, sentiment))

        entry_id = self.cursor.lastrowid # getting the primary key of the row we just inserted
        
        query = """INSERT INTO embeddings (entry_id, content_embedding) VALUES (?, ?)"""
        self.run_query(query=query, parameters=(entry_id, content_embedding))
    
    def insert(self, prompt, title, content, sentiment, content_embedding):
        query = """INSERT INTO entries (prompt, title, content, sentiment) VALUES (?, ?, ?, ?)"""
        self.run_query(query=query, parameters=(prompt, title, content, sentiment))
        
        entry_id = self.cursor.lastrowid # getting the primary key of the row we just inserted
        
        query = """INSERT INTO embeddings (entry_id, content_embedding) VALUES (?, ?)"""
        self.run_query(query=query, parameters=(entry_id, content_embedding))

    def update(self, entry_id, title, prompt, content, sentiment, content_embedding):
        query = """UPDATE entries SET title = ?, prompt = ?, content = ?, sentiment = ? WHERE entry_id = ?"""
        self.run_query(query=query, parameters=(title, prompt, content, sentiment, entry_id))

        embedding_query = """UPDATE embeddings SET content_embedding = ? WHERE entry_id = ?"""
        self.run_query(query=embedding_query, parameters=(content_embedding, entry_id))

    def delete(self, entry_id):
        self.run_query("""DELETE FROM entries WHERE entry_id = ?""", (entry_id,))
        self.run_query("""DELETE FROM embeddings WHERE entry_id = ?""", (entry_id,))

    def run_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def run_query(self, query, parameters):
        self.cursor.execute(query, parameters)
        result = self.cursor.fetchall()
        return result