# setup_and_run.ps1 - Create venv, install deps, install package editable, and run example
# Usage: Open PowerShell in project root and run: .\scripts\setup_and_run.ps1

$venvPath = Join-Path $PWD '.venv'

if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment at $venvPath..."
    python -m venv $venvPath
} else {
    Write-Host "Virtual environment already exists at $venvPath"
}

$python = Join-Path $venvPath 'Scripts\python.exe'

Write-Host "Upgrading pip and installing requirements..."
& $python -m pip install --upgrade pip
& $python -m pip install -r requirements.txt

Write-Host "Installing package in editable mode..."
& $python -m pip install -e .

Write-Host "Running example script..."
& $python examples\basic_usage.py

Write-Host "Done. Check ./examples/output for results." 
