# Windows Startup Applications Launcher
# Automatically launches your work applications when Windows starts

# Define applications to launch
$applications = @(
    @{
        Name = "Microsoft Word"
        Path = "C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
        BackupPath = "C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE"
    },
    @{
        Name = "Visual Studio Code"
        Path = "$env:LOCALAPPDATA\Programs\Microsoft VS Code\Code.exe"
        BackupPath = "C:\Program Files\Microsoft VS Code\Code.exe"
        Arguments = "C:\Users\grego\Documents\SEAL Enterprises\Website Code\seal-site\V1-play"
    },
    @{
        Name = "PowerShell"
        Path = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        Arguments = "-NoExit -Command `"cd 'C:\Users\grego\Documents\SEAL Enterprises\Website Code\seal-site\V1-play'`""
    }
)

Write-Host "Launching startup applications..." -ForegroundColor Cyan

foreach ($app in $applications) {
    # Find the executable
    $exePath = $null
    if (Test-Path $app.Path) {
        $exePath = $app.Path
    } elseif ($app.BackupPath -and (Test-Path $app.BackupPath)) {
        $exePath = $app.BackupPath
    }
    
    if ($exePath) {
        Write-Host "Starting $($app.Name)..." -ForegroundColor Green
        
        if ($app.Arguments) {
            Start-Process $exePath -ArgumentList $app.Arguments
        } else {
            Start-Process $exePath
        }
        
        # Small delay between launches
        Start-Sleep -Milliseconds 500
    } else {
        Write-Host "Could not find $($app.Name)" -ForegroundColor Yellow
    }
}

Write-Host "All applications launched!" -ForegroundColor Green
