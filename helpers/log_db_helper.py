import sqlite3

DB_PATH = 'logs.db'

def count_info_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM log_entries WHERE level = 'INFO'")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def count_logs_by_level(level):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM log_entries WHERE level = ?", (level,))
    count = cursor.fetchone()[0]
    conn.close()
    return count
