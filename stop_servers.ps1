# Stop servers started by background script

$ErrorActionPreference = "Continue"

Write-Host "Stopping SEAL Contact Form Servers..." -ForegroundColor Yellow

$WorkDir = $PSScriptRoot

# Stop Flask server
$flaskPidFile = Join-Path $WorkDir ".flask_pid"
if (Test-Path $flaskPidFile) {
    $flaskPid = Get-Content $flaskPidFile
    try {
        Stop-Process -Id $flaskPid -Force -ErrorAction Stop
        Write-Host "✓ Stopped Flask server (PID: $flaskPid)" -ForegroundColor Green
    } catch {
        Write-Host "Flask server already stopped or not found" -ForegroundColor Gray
    }
    Remove-Item $flaskPidFile -Force
}

# Stop HTTP server
$httpPidFile = Join-Path $WorkDir ".http_pid"
if (Test-Path $httpPidFile) {
    $httpPid = Get-Content $httpPidFile
    try {
        Stop-Process -Id $httpPid -Force -ErrorAction Stop
        Write-Host "✓ Stopped HTTP server (PID: $httpPid)" -ForegroundColor Green
    } catch {
        Write-Host "HTTP server already stopped or not found" -ForegroundColor Gray
    }
    Remove-Item $httpPidFile -Force
}

# Also check for any python processes running server.py
Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*server.py*"
} | ForEach-Object {
    Stop-Process -Id $_.Id -Force
    Write-Host "✓ Stopped Python process (PID: $($_.Id))" -ForegroundColor Green
}

# Check for any http-server node processes
Get-Process node -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*http-server*"
} | ForEach-Object {
    Stop-Process -Id $_.Id -Force
    Write-Host "✓ Stopped HTTP server process (PID: $($_.Id))" -ForegroundColor Green
}

Write-Host "`nServers stopped!" -ForegroundColor Green
