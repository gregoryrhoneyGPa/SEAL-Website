$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Push-Location (Join-Path $scriptDir '..')
# Start a new PowerShell window that runs the HTTP server so this script can exit.
$serverCommand = 'python -m http.server 8000'
Start-Process -FilePath powershell -ArgumentList "-NoExit","-Command",$serverCommand
Start-Sleep -Seconds 1
Start-Process "http://localhost:8000/Index.html"
Pop-Location
