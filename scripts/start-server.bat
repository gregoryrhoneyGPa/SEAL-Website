@echo off
pushd "%~dp0\.."
start powershell -NoExit -Command "python -m http.server 8000"
start "" "http://localhost:8000/Index.html"
popd
