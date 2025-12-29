# Remove automatic startup task from Windows Task Scheduler
# Run this script as Administrator to disable automatic startup

$ErrorActionPreference = "Stop"

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "Remove SEAL Automatic Startup" -ForegroundColor Cyan
Write-Host "=========================================`n" -ForegroundColor Cyan

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  This script needs to run as Administrator!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

$TaskName = "SEAL Contact Form Servers"

# Check if task exists
$task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($task) {
    Write-Host "Found task: $TaskName" -ForegroundColor Yellow
    Write-Host "Removing..." -ForegroundColor Yellow
    
    # Stop servers first
    Write-Host "Stopping any running servers..." -ForegroundColor Cyan
    & "$PSScriptRoot\stop_servers.ps1"
    
    # Remove scheduled task
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    
    Write-Host "`n✅ Automatic startup disabled!" -ForegroundColor Green
    Write-Host "Servers will no longer start automatically.`n" -ForegroundColor White
} else {
    Write-Host "Task '$TaskName' not found." -ForegroundColor Yellow
    Write-Host "Automatic startup was not configured.`n" -ForegroundColor White
}

Read-Host "Press Enter to exit"
