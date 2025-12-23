$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Push-Location (Join-Path $scriptDir '..')
python .\tools\basic_a11y_check.py
Pop-Location
Pause
