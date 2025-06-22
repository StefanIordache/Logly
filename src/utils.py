import os

# Check if there are any changes in the log file (offset and state file based)
def detect_log_file_change(filepath, last_offset):
    try:
        return os.path.getsize(filepath) > last_offset
    except FileNotFoundError:
        return False

# Read lines batch by batch
def read_batch(file_obj, batch_size):
    batch = []
    for line in file_obj:
        if line.strip():
            batch.append(line)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch