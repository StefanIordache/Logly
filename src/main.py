import os
import yaml
import json
from processor import process_logs
from utils import detect_log_file_change

CONFIG_FILE = "config.yml"
STATE_FILE = "state.json"
CHECK_INTERVAL = 1
         
# Configuration loader function                               
def load_config():
    with open(CONFIG_FILE) as cfg:
        return yaml.safe_load(cfg)
   
# State utils for an agent like application.
# We would like to keep track of the progress made by our log parser. 
def load_state():
    try:
        with open(STATE_FILE) as statefile:
            return json.load(statefile)
    except FileNotFoundError:
        return {"files": {}}

def save_state(state):
    with open(STATE_FILE, "w") as statefile:
        json.dump(state, statefile)                                  
                                 
"""
Main function used for log processing
"""
def main():
    config = load_config()
    state = load_state()
    
    while True:
        for entry in config.get("logs", []):
            log_file_path = entry["log_file_path"]
            batch_size = int(entry.get("batch_size", 20))
            warning_threshold = int(entry["warning_threshold"])
            error_threshold = int(entry["error_threshold"])
            warning_file_path = entry["warning_file_path"]
            error_file_path = entry["error_file_path"]
            
            offset = state["files"].get(log_file_path, {}).get("offset", 0)
            active = state["files"].get(log_file_path, {}).get("active_jobs", {})
            
            if detect_log_file_change(log_file_path, offset):
                result = process_logs(log_file_path, offset, active, batch_size, warning_threshold, error_threshold, warning_file_path, error_file_path)
                state["files"][log_file_path] = {
                    "offset": result["offset"],
                    "active_jobs": result["active_jobs"]
                }
                save_state(state)
            

if __name__ == "__main__":
    main()
