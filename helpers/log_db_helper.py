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

def get_log_level_counts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT level, COUNT(*) FROM log_entries GROUP BY level")
    results = cursor.fetchall()
    conn.close()
    return {level: count for level, count in results}

def get_log_level_heatmap():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT level, substr(timestamp, 12, 2) as hour, COUNT(*)
        FROM log_entries
        GROUP BY level, hour
        ORDER BY level, hour
    """)
    results = cursor.fetchall()
    conn.close()
    # Structure: {level: {hour: count}}
    heatmap = {}
    for level, hour, count in results:
        if level not in heatmap:
            heatmap[level] = {}
        heatmap[level][hour] = count
    return heatmap

def get_log_trendline():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Group by date (YYYY-MM-DD) for daily trend
    cursor.execute("SELECT substr(timestamp, 1, 10) as date, COUNT(*) FROM log_entries GROUP BY date ORDER BY date")
    results = cursor.fetchall()
    conn.close()
    # Returns list of (date, count)
    return {'dates': [row[0] for row in results], 'counts': [row[1] for row in results]}
