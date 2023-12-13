import sqlite3

with sqlite3.connect('Data.db') as db:
    cursor = db.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS events
        (
        chatID INTEGER, 
        event_day INTEGER,
        event TEXT
        ) """)

    db.commit()
