# PowerShell script to start both servers

Write-Host "Starting SEAL Website Servers..." -ForegroundColor Green
Write-Host ""

# Start Flask server in a new window
Write-Host "Starting Flask backend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; & '$PSScriptRoot\.venv\Scripts\python.exe' server.py"

# Wait a moment for Flask to start
Start-Sleep -Seconds 2

# Start HTTP server in a new window
Write-Host "Starting HTTP server for website..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; npx http-server -c-1 . -p 8000"

Write-Host ""
Write-Host "Servers started!" -ForegroundColor Green
Write-Host "Flask API: http://localhost:5000" -ForegroundColor Yellow
Write-Host "Website: http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Test the contact form at: http://localhost:8000/contact.html" -ForegroundColor Magenta
Write-Host "Form submissions will be saved to: docs\contact_submissions.xlsx" -ForegroundColor Magenta
