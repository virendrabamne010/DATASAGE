@echo off
REM Run example: create venv, install deps, install package, run example
IF NOT EXIST .venv (
    python -m venv .venv
)
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\python.exe examples\basic_usage.py
pause
