# Background server launcher - runs servers without visible windows
# This script is designed to run at Windows startup

$ErrorActionPreference = "Stop"
$LogFile = Join-Path $PSScriptRoot "server_startup.log"

function Write-Log {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -FilePath $LogFile -Append
    Write-Host $Message
}

Write-Log "========================================="
Write-Log "Starting SEAL Contact Form Servers"
Write-Log "========================================="

$WorkDir = $PSScriptRoot

# Start Flask backend server
try {
    Write-Log "Starting Flask backend server..."
    $pythonPath = Join-Path $WorkDir ".venv\Scripts\python.exe"
    $serverScript = Join-Path $WorkDir "server.py"
    
    $flaskProcess = Start-Process -FilePath $pythonPath `
        -ArgumentList $serverScript `
        -WorkingDirectory $WorkDir `
        -WindowStyle Hidden `
        -PassThru
    
    Write-Log "Flask server started (PID: $($flaskProcess.Id))"
    
    # Save PID for later management
    $flaskProcess.Id | Out-File -FilePath (Join-Path $WorkDir ".flask_pid") -Force
    
} catch {
    Write-Log "ERROR starting Flask server: $_"
}

# Wait for Flask to initialize
Start-Sleep -Seconds 3

# Start HTTP server for website
try {
    Write-Log "Starting HTTP server for website..."
    
    $httpProcess = Start-Process -FilePath "npx" `
        -ArgumentList "http-server", "-c-1", ".", "-p", "8000" `
        -WorkingDirectory $WorkDir `
        -WindowStyle Hidden `
        -PassThru
    
    Write-Log "HTTP server started (PID: $($httpProcess.Id))"
    
    # Save PID for later management
    $httpProcess.Id | Out-File -FilePath (Join-Path $WorkDir ".http_pid") -Force
    
} catch {
    Write-Log "ERROR starting HTTP server: $_"
}

Write-Log "========================================="
Write-Log "Servers started successfully!"
Write-Log "Flask API: http://localhost:5000"
Write-Log "Website: http://localhost:8000"
Write-Log "Log file: $LogFile"
Write-Log "========================================="
