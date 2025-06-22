"""
THIS IS A DRAFT IMPLEMENTATION! TO ACHIEVE:
    - Read and parse log file
    - Use two data structures
        - One collection for tracking in progress / active tasks (should be optimized as a hash table or dictionary)
        - One collection for keeping completed tasks in memory. We are going to process this list at the end or during file reading and processing
    - Implement core logic for START and END actions
"""

from datetime import datetime
import os

# Input & output files
log_file = "data/logs.log"
output_dir = "output"
warning_file = os.path.join(output_dir, "warnings.log")
error_file = os.path.join(output_dir, "errors.log")

# Warning threshold - 5 minutes = 300 seconds
WARNING_THRESHOLD = 300

# Error threshold - 10 minutes = 600 seconds
ERROR_THRESHOLD = 600

# Check if output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read log file
with open(log_file, "r") as f:
    lines = f.readlines()

"""
Data structures required
   - Active jobs (dictionary)
   - Completed jobs (list)
"""
active_jobs = {}
completed_jobs = []

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
for line in lines:
    if not line.strip():
        continue
    parts = [p.strip() for p in line.strip().split(",")]
    timestamp, description, action, pid = parts
    if action == "START":
        active_jobs[pid] = {"description": description, "start": timestamp}
    elif action == "END" and pid in active_jobs:
        start_time = parse_time(active_jobs[pid]["start"])
        end_time = parse_time(timestamp)
        duration = (end_time - start_time).total_seconds()
        completed_jobs.append((pid, description, active_jobs[pid]["start"], timestamp, duration))
        del active_jobs[pid]

# Write warning (wf) and errors (ef) into two different files / streams
with open(warning_file, "w") as wf, open(error_file, "w") as ef:
    for pid, description, start, end, duration in completed_jobs:
        if duration > ERROR_THRESHOLD:
            ef.write(f"[ERROR] {description} (PID {pid}): {int(duration)}s from {start} to {end}\n")
        elif duration > WARNING_THRESHOLD:
            wf.write(f"[WARNING] {description} (PID {pid}): {int(duration)}s from {start} to {end}\n")