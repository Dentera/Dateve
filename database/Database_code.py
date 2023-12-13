import sqlite3

db = sqlite3.connect('Data.db', check_same_thread=False)
cursor = db.cursor()
cursor.execute(""" CREATE TABLE IF NOT EXISTS events
    (
    chatID INTEGER, 
    event_day INTEGER,
    event TEXT
    ) """)

db.commit()
