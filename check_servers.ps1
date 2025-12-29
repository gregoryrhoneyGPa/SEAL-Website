# Check if servers are running and display status

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "SEAL Contact Form Servers - Status" -ForegroundColor Cyan
Write-Host "=========================================`n" -ForegroundColor Cyan

# Check Flask server (Python)
$flaskRunning = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*server.py*"
}

if ($flaskRunning) {
    Write-Host "✅ Flask Server: RUNNING (PID: $($flaskRunning.Id))" -ForegroundColor Green
    Write-Host "   URL: http://localhost:5000" -ForegroundColor Yellow
} else {
    Write-Host "❌ Flask Server: NOT RUNNING" -ForegroundColor Red
}

# Check HTTP server (Node)
$httpRunning = Get-Process node -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*http-server*"
}

if ($httpRunning) {
    Write-Host "✅ HTTP Server: RUNNING (PID: $($httpRunning.Id))" -ForegroundColor Green
    Write-Host "   URL: http://localhost:8000" -ForegroundColor Yellow
    Write-Host "   Contact Form: http://localhost:8000/contact.html" -ForegroundColor Magenta
} else {
    Write-Host "❌ HTTP Server: NOT RUNNING" -ForegroundColor Red
}

# Check scheduled task
Write-Host ""
$task = Get-ScheduledTask -TaskName "SEAL Contact Form Servers" -ErrorAction SilentlyContinue
if ($task) {
    $taskState = $task.State
    if ($taskState -eq "Ready") {
        Write-Host "✅ Autostart: ENABLED" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Autostart: ENABLED but state is $taskState" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Autostart: NOT CONFIGURED" -ForegroundColor Yellow
    Write-Host "   Run setup_autostart.ps1 to enable" -ForegroundColor Gray
}

# Check log file
$logFile = Join-Path $PSScriptRoot "server_startup.log"
if (Test-Path $logFile) {
    Write-Host "`nRecent Log Entries:" -ForegroundColor Cyan
    Get-Content $logFile -Tail 5 | ForEach-Object {
        Write-Host "   $_" -ForegroundColor Gray
    }
}

Write-Host "`n=========================================`n" -ForegroundColor Cyan

# Check URLs
if ($flaskRunning -and $httpRunning) {
    Write-Host "🎉 Both servers running! Test the form:" -ForegroundColor Green
    Write-Host "   http://localhost:8000/contact.html`n" -ForegroundColor Magenta
} elseif (-not $flaskRunning -and -not $httpRunning) {
    Write-Host "To start servers:" -ForegroundColor Yellow
    Write-Host "   .\start_servers.ps1   (interactive)" -ForegroundColor White
    Write-Host "   .\start_servers_background.ps1   (background)`n" -ForegroundColor White
}
