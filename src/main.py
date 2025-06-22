import os
import yaml
from processor import process_logs

CONFIG_FILE = "config.yml"
                                 
def load_config():
    with open(CONFIG_FILE) as cfg:
        return yaml.safe_load(cfg)                              
                                 
"""
Main function used for log processing
"""
def main():
    config = load_config()
    
    for entry in config.get("logs", []):
        print(entry)
        log_file_path = entry["log_file_path"]
        warning_threshold = int(entry["warning_threshold"])
        error_threshold = int(entry["error_threshold"])
        warning_file_path = entry["warning_file_path"]
        error_file_path = entry["error_file_path"]
        result = process_logs(log_file_path, warning_threshold, error_threshold, warning_file_path, error_file_path)

if __name__ == "__main__":
    main()
