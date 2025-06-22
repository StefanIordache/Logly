# Logly – Lightweight Log Monitoring Agent

**Logly** is a Python 3.10+ project designed to monitor log files and detect long-running jobs. It was initially built as a coding challenge and evolved incrementally from a simple, hardcoded version to a modular, file-based and agentic log processor.

---

## 🚀 Core Functionality

Logly reads a structured log file with lines like:

```
HH:MM:SS, job description, START|END, PID
```

It:
- Detects job durations by pairing `START` and `END` entries using their `PID`
- Logs a `WARNING` if a job runs longer than 5 minutes
- Logs an `ERROR` if it exceeds 10 minutes
- Saves warnings and errors in separate output files

---

## 📁 Project Structure

```
logly/
├── src/
│   ├── main.py            # Entry point for execution
│   ├── processor.py       # Core logic for parsing and duration detection
│   ├── utils.py           # Helper functions
│   ├── config.yml         # YAML config (optional, not used in v0)
│   ├── state.json         # Saved state (for later versions)
├── data/
│   └── logs.log           # Example input log file
├── output/
│   ├── warnings.log       # Output: warnings >5min
│   └── errors.log         # Output: errors >10min
├── tests/                 # Tests directory
│   ├── test_utils.py
│   ├── test_processor.py
│   └── test_main.py
├── draft.py               # Early version of the agent (v0)
├── requirements.txt       # Required packages (minimal)
└── README.md              # You are here 🙂
```

---

## 🧪 How to Run the Project

Ensure Python 3.10+ is installed. You don’t need any external dependencies for the base version.

### Step-by-step:
```bash
# (Optional) Remove old state/output files
rm -f src/state.json output/warnings.log output/errors.log

# Run the main processor
python3 src/main.py
```

Logly will read the file `data/logs.log`, process all jobs, and generate:
- `output/warnings.log`
- `output/errors.log`

---

## 🔄 Evolution Notes

This project started as a minimal, hardcoded script with:
- No batching
- No threading
- No config

Over time, it evolved into a more modular agentic approach, including:
- state tracking
- YAML configuration
- utility separation

This README documents the latest stable state of the base version.

---

## ⚙️ Requirements

- Python 3.10+
- (Optional for future versions) `pyyaml`

Install dependencies (if any) via:

```bash
pip install -r requirements.txt
```

## 🧪 Running Tests

Logly includes basic unit tests for core modules (`utils.py`, `processor.py`, `main.py`) using `pytest`.

### ✅ Requirements

- Python 3.10+
- `pytest` installed

```bash
pip install pytest
```

### 📂 Test Directory Structure

```
logly/
├── src/
│   ├── main.py
│   └── ...
├── tests/
│   ├── test_utils.py
│   ├── test_processor.py
│   └── test_main.py
```

### 🚀 Run All Tests

```bash
PYTHONPATH=./src pytest tests/
```

Or for more verbose output:

```bash
PYTHONPATH=./src pytest -v tests/
```

### 🔍 What is tested?

- ✅ `utils.py` — batch reading & file change detection
- ✅ `processor.py` — line parsing and time parsing
- ✅ `main.py` — module imports correctly

## 🔮 Future Work

The current version of Logly serves as a foundational implementation. Several enhancements can be considered for future iterations:

- **Support for multiple log files**: Add multithreaded or asynchronous processing to watch several files in parallel.
- **Web UI or dashboard**: Visualize running jobs, alerts, and history with filtering capabilities.
- **Packaging as CLI**: Allow running Logly via `pip install` and `logly --config config.yml`.
- **Agent & Service**: Develop the module further and implement it like CloudWatch agent.

---

## 📜 License

MIT License – use freely and build upon it.