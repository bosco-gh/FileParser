import re
from models.log_entry import LogEntry
from data.database import Database

class LogController:
    def __init__(self, db_path='logs.db'):
        self.db = Database(db_path)

    def parse_log_line(self, line):
        match = re.match(r'^(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (?P<level>\w+) (?P<msg>.+)$', line)
        if match:
            return LogEntry(
                timestamp=match.group('date'),
                level=match.group('level'),
                message=match.group('msg')
            )
        return None

    def process_log_file(self, file_path_or_obj):
        if isinstance(file_path_or_obj, str):
            f = open(file_path_or_obj, 'r')
            close_after = True
        else:
            f = file_path_or_obj
            close_after = False
        try:
            for line in f:
                print (f"Processing line: {line.strip()}")
                entry = self.parse_log_line(line.strip())
                print(f"Parsed log entry: {entry.timestamp} [{entry.level}] {entry.message}" if entry else "Failed to parse line")
                if entry:
                    self.db.insert_log_entry(entry)
        finally:
            if close_after:
                f.close()
