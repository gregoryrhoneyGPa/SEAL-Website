# Setup Windows Startup Applications
# Adds your work applications to Windows startup

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$startupScript = Join-Path $scriptPath "startup_apps.ps1"
$startupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$shortcutPath = Join-Path $startupFolder "LaunchWorkApps.lnk"

Write-Host ""
Write-Host "Windows Startup Applications Setup" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Create shortcut in Startup folder
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$startupScript`""
$Shortcut.WorkingDirectory = $scriptPath
$Shortcut.Description = "Launch work applications"
$Shortcut.Save()

Write-Host "Startup shortcut created!" -ForegroundColor Green
Write-Host ""
Write-Host "Applications that will launch on startup:" -ForegroundColor Cyan
Write-Host "  - Microsoft Word" -ForegroundColor White
Write-Host "  - Visual Studio Code (opens V1-play folder)" -ForegroundColor White
Write-Host "  - PowerShell (opens in V1-play folder)" -ForegroundColor White
Write-Host ""
Write-Host "Shortcut location: $shortcutPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "To disable: Delete the shortcut from:" -ForegroundColor Yellow
Write-Host "  $startupFolder" -ForegroundColor White
Write-Host ""

# Test it now?
Write-Host "Test launch now? (Y/N): " -ForegroundColor Cyan -NoNewline
$response = Read-Host

if ($response -eq 'Y' -or $response -eq 'y') {
    Write-Host ""
    & $startupScript
}
