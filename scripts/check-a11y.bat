@echo off
pushd "%~dp0\.."
python tools\basic_a11y_check.py
popd
pause
