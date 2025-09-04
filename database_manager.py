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
    
    def run_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result