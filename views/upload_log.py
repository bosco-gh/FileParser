import sys
from controllers.log_controller import LogController

def main():
    if len(sys.argv) < 2:
        print('Usage: python views/upload_log.py <log_file_path>')
        return
    log_file = sys.argv[1]
    print(f'Processing log file: {log_file}')
    controller = LogController()
    controller.process_log_file(log_file)
    print('Log file processed and data inserted into SQLite database.')

if __name__ == '__main__':
    main()
