import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from utils import detect_log_file_change, read_batch
import tempfile
import os

def test_detect_log_file_change_detects_growth():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write("line1\n")
        tmp.flush()
        initial_size = os.path.getsize(tmp.name)
        tmp.write("line2\n")
        tmp.flush()
        assert detect_log_file_change(tmp.name, initial_size) is True

def test_read_batch_yields_correct_batches():
    lines = ["a\n", "b\n", "c\n", "d\n"]
    batches = list(read_batch(iter(lines), 2))
    assert batches == [["a\n", "b\n"], ["c\n", "d\n"]]