# Setup automatic startup using Windows Task Scheduler
# Run this script as Administrator to set up automatic server startup

$ErrorActionPreference = "Stop"

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "SEAL Contact Form - Automatic Startup Setup" -ForegroundColor Cyan
Write-Host "=========================================`n" -ForegroundColor Cyan

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  This script needs to run as Administrator!" -ForegroundColor Red
    Write-Host "`nTo run as Administrator:" -ForegroundColor Yellow
    Write-Host "1. Right-click PowerShell" -ForegroundColor Yellow
    Write-Host "2. Select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host "3. Navigate to this folder:" -ForegroundColor Yellow
    Write-Host "   cd '$PSScriptRoot'" -ForegroundColor Yellow
    Write-Host "4. Run: .\setup_autostart.ps1`n" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

$WorkDir = $PSScriptRoot
$ScriptPath = Join-Path $WorkDir "start_servers_background.ps1"

Write-Host "Setting up Windows Task Scheduler...`n" -ForegroundColor Cyan

# Task details
$TaskName = "SEAL Contact Form Servers"
$TaskDescription = "Automatically starts Flask and HTTP servers for SEAL contact form"

# Remove existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create action
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$ScriptPath`"" `
    -WorkingDirectory $WorkDir

# Create trigger (at system startup)
$trigger = New-ScheduledTaskTrigger -AtStartup

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

# Create principal (run as current user)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

# Register the task
try {
    Register-ScheduledTask -TaskName $TaskName `
        -Description $TaskDescription `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Force | Out-Null
    
    Write-Host "✅ Task created successfully!" -ForegroundColor Green
    Write-Host "`nTask Details:" -ForegroundColor Cyan
    Write-Host "  Name: $TaskName" -ForegroundColor White
    Write-Host "  Trigger: At system startup" -ForegroundColor White
    Write-Host "  Script: $ScriptPath" -ForegroundColor White
    
    Write-Host "`nWhat happens now:" -ForegroundColor Cyan
    Write-Host "  • Servers will start automatically when Windows starts" -ForegroundColor White
    Write-Host "  • If a server crashes, it will restart automatically" -ForegroundColor White
    Write-Host "  • Runs in background (no windows)" -ForegroundColor White
    Write-Host "  • Logs to: server_startup.log" -ForegroundColor White
    
    Write-Host "`nManage the task:" -ForegroundColor Cyan
    Write-Host "  • Open Task Scheduler: taskschd.msc" -ForegroundColor White
    Write-Host "  • Find task: Task Scheduler Library > $TaskName" -ForegroundColor White
    Write-Host "  • Stop servers manually: .\stop_servers.ps1" -ForegroundColor White
    
    Write-Host "`nTest it now:" -ForegroundColor Cyan
    Write-Host "  • Start manually: Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
    Write-Host "  • Check status: Get-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
    Write-Host "  • View log: Get-Content server_startup.log -Tail 20" -ForegroundColor White
    
    Write-Host "`n" -ForegroundColor Green
    $runNow = Read-Host "Would you like to start the servers now? (Y/N)"
    
    if ($runNow -eq 'Y' -or $runNow -eq 'y') {
        Write-Host "`nStarting servers..." -ForegroundColor Cyan
        Start-ScheduledTask -TaskName $TaskName
        Start-Sleep -Seconds 3
        Write-Host "✅ Servers started!" -ForegroundColor Green
        Write-Host "  Flask API: http://localhost:5000" -ForegroundColor Yellow
        Write-Host "  Website: http://localhost:8000" -ForegroundColor Yellow
        Write-Host "  Contact Form: http://localhost:8000/contact.html" -ForegroundColor Magenta
    }
    
} catch {
    Write-Host "❌ Error creating task: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n=========================================`n" -ForegroundColor Cyan
Read-Host "Press Enter to exit"
