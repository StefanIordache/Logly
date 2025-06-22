import os
from processor import process_logs

OUTPUT_DIR = "../output"
LOG_FILE_PATH = "../data/logs.log"
ERROR_FILE_PATH = os.path.join(OUTPUT_DIR, "errors.log")
WARNING_FILE_PATH = os.path.join(OUTPUT_DIR, "warnings.log")

"""
Main function used for log processing
"""
def main():
    result = process_logs(LOG_FILE_PATH, WARNING_FILE_PATH, ERROR_FILE_PATH)

if __name__ == "__main__":
    main()