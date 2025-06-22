from datetime import datetime
from utils import read_batch

"""
Data structures required
   - Active jobs (dictionary)
   - Completed jobs (list)
"""
active_jobs = {}
completed_jobs = []


# Parses a complete line of logs and extracts components
def parse_line(line):
    parts = [p.strip() for p in line.split(",")]
    return {
        "timestamp": parts[0],
        "description": parts[1],
        "action": parts[2],
        "pid": parts[3]
    }


# Parses a time string in HH:MM:SS format and returns a datetime object
def parse_time(t):
    return datetime.strptime(t, "%H:%M:%S")

"""
Log processing, line by line
    - Try and read line
    - Strip and split each line based on ',' delimiter
    - Extract components: timestamp, description, action and pid
    - Add job into active_jobs dictionary if action is 'START'
    - If action is END 
        - Compute total duration after parsing timestamps
        - Append to completed_jobs to keep track of finished tasks
        - Remove ended task from active_jobs (PID might be reused and we cannot leave it in the collection of active jobs)
"""
def process_logs(logs_filepath, offset, active, batch_size, warning_threshold, error_threshold, output_warning_filepath, output_error_filepath):
    with open(logs_filepath, "r") as f:
        f.seek(offset)
        for batch in read_batch(f, batch_size):
            completed_jobs = []
            for line in batch:
                if not line.strip():
                    continue
                parsed_line = parse_line(line)
                timestamp, description, action, pid = parsed_line["timestamp"], parsed_line["description"], parsed_line["action"], parsed_line["pid"]
                if action == "START":
                    active_jobs[pid] = {"description": description, "start": timestamp}
                elif action == "END" and pid in active_jobs:
                    start_time = parse_time(active_jobs[pid]["start"])
                    end_time = parse_time(timestamp)
                    duration = (end_time - start_time).total_seconds()
                    completed_jobs.append((pid, description, active_jobs[pid]["start"], timestamp, duration))
                    del active_jobs[pid]
                
            # Write warnings (wf) and errors (ef) into two different files / streams
            with open(output_warning_filepath, "a+") as wf, open(output_error_filepath, "a+") as ef:
                for pid, description, start, end, duration in completed_jobs:
                    if duration > error_threshold:
                        ef.write(f"[ERROR] {description} (PID {pid}): {int(duration)}s from {start} to {end}\n")
                    elif duration > warning_threshold:
                        wf.write(f"[WARNING] {description} (PID {pid}): {int(duration)}s from {start} to {end}\n")
                        
        return {"offset": f.tell(), "active_jobs": active_jobs}