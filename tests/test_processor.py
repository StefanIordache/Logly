import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from processor import parse_line, parse_time

def test_parse_line_valid():
    line = "12:34:56, test job, START, 99999"
    parsed = parse_line(line)
    assert parsed["timestamp"] == "12:34:56"
    assert parsed["description"] == "test job"
    assert parsed["action"] == "START"
    assert parsed["pid"] == "99999"

def test_parse_time_returns_datetime():
    from datetime import datetime
    result = parse_time("00:00:01")
    assert isinstance(result, datetime)
    assert result.hour == 0
    assert result.minute == 0
    assert result.second == 1