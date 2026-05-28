import sqlite3

class Database:
    def __init__(self, db_path='logs.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS log_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            level TEXT,
            message TEXT
        )''')
        self.conn.commit()

    def insert_log_entry(self, log_entry):
        self.conn.execute(
            'INSERT INTO log_entries (timestamp, level, message) VALUES (?, ?, ?)',
            (log_entry.timestamp, log_entry.level, log_entry.message)
        )
        self.conn.commit()
