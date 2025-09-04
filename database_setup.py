import sqlite3
import sqlite_vec

# define connection
connection = sqlite3.connect("moment.db")
connection.execute("PRAGMA foreign_keys = ON")  # need this after every connection

connection.enable_load_extension(True)
sqlite_vec.load(connection) # adding loading up the sqlite extention for vectors
connection.enable_load_extension(False)
    
cursor = connection.cursor()

# create journal entries table
entriesTable = """CREATE VIRTUAL TABLE IF NOT EXISTS entries USING
vec0(entry_id INTEGER PRIMARY KEY AUTOINCREMENT, prompt TEXT, title TEXT, content TEXT, date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP, sentiments TEXT, content_embedding float[384])"""
# CANT have 2 vectors in 1 table - sentiment embedding is a json string in that case
# make sure content_embedding is always fr a float[384]
# can do OFFSET 10 and LIMIT 5 on queries
# TODO: add actual dummy data to this

# executing command
cursor.execute(entriesTable)

# persisting changes to the database
connection.commit()
connection.close()