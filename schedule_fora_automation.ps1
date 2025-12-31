# Schedule FORA Automation Script
# Runs the automation on a schedule using Windows Task Scheduler

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptPath "fora_automation.py"
$venvPython = Join-Path $scriptPath ".venv\Scripts\python.exe"
$logFile = Join-Path $scriptPath "automation_scheduler.log"

Write-Host "FORA Automation Scheduler" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path $venvPython)) {
    Write-Host "Error: Python virtual environment not found" -ForegroundColor Red
    Write-Host "Expected at: $venvPython" -ForegroundColor Yellow
    Write-Host "Please run: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Install required packages
Write-Host "Installing required Python packages..." -ForegroundColor Green
& $venvPython -m pip install requests beautifulsoup4 mailchimp-marketing --quiet

# Create scheduled task
$taskName = "FORA_Travel_Automation"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
$action = New-ScheduledTaskAction -Execute $venvPython -Argument $pythonScript -WorkingDirectory $scriptPath
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd

Write-Host ""
Write-Host "Creating scheduled task: $taskName" -ForegroundColor Green
Write-Host "Schedule: Daily at 9:00 AM" -ForegroundColor Yellow
Write-Host "Script: $pythonScript" -ForegroundColor Yellow

try {
    # Remove existing task if present
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    
    # Register new task
    Register-ScheduledTask -TaskName $taskName -Trigger $trigger -Action $action -Settings $settings -Description "Automatically fetch FORA travel guides and sync with Mailchimp"
    
    Write-Host ""
    Write-Host "✓ Scheduled task created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "The automation will run daily at 9:00 AM" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To run manually now:" -ForegroundColor Yellow
    Write-Host "  python fora_automation.py" -ForegroundColor White
    Write-Host ""
    Write-Host "To view scheduled tasks:" -ForegroundColor Yellow
    Write-Host "  Get-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
    Write-Host ""
    Write-Host "To disable automation:" -ForegroundColor Yellow
    Write-Host "  Disable-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "Error creating scheduled task: $_" -ForegroundColor Red
    exit 1
}

# Test run option
Write-Host "Would you like to run a test now? (Y/N): " -ForegroundColor Cyan -NoNewline
$response = Read-Host

if ($response -eq 'Y' -or $response -eq 'y') {
    Write-Host ""
    Write-Host "Running test automation..." -ForegroundColor Green
    Write-Host ""
    & $venvPython $pythonScript
}
