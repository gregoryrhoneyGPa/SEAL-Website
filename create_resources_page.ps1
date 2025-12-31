# Quick Resources Page Generator
# Creates a beautiful travel resources directory from your FORA guides

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $scriptPath ".venv\Scripts\python.exe"
$generatorScript = Join-Path $scriptPath "generate_resources_page.py"
$csvFile = Join-Path $scriptPath "fora_guides.csv"

Write-Host ""
Write-Host "FORA Travel Resources Page Generator" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if CSV exists
if (-not (Test-Path $csvFile)) {
    Write-Host "CSV file not found: fora_guides.csv" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please export your FORA Google Sheet:" -ForegroundColor Yellow
    Write-Host "   1. Open your FORA shareable assets sheet" -ForegroundColor White
    Write-Host "   2. Click: File -> Download -> CSV (.csv)" -ForegroundColor White
    Write-Host "   3. Save as: fora_guides.csv" -ForegroundColor White
    Write-Host "   4. Move to: $scriptPath" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Show CSV info
$csvAge = (Get-Item $csvFile).LastWriteTime
$ageHours = ((Get-Date) - $csvAge).TotalHours

Write-Host "CSV File: " -ForegroundColor Green -NoNewline
Write-Host "fora_guides.csv" -ForegroundColor White
Write-Host "Last Updated: " -ForegroundColor Green -NoNewline
Write-Host "$csvAge" -ForegroundColor White

# Check virtual environment
if (-not (Test-Path $venvPython)) {
    Write-Host "Python virtual environment not found" -ForegroundColor Red
    exit 1
}

# Generate page
Write-Host ""
Write-Host "Generating resources page..." -ForegroundColor Cyan
Write-Host ""

& $venvPython $generatorScript

$exitCode = $LASTEXITCODE

Write-Host ""

if ($exitCode -eq 0) {
    Write-Host ""
    Write-Host "Resources page generated!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Created files:" -ForegroundColor Cyan
    Write-Host "   - resources.html (main page)" -ForegroundColor White
    Write-Host "   - fora_guides_catalog.json (data)" -ForegroundColor White
    Write-Host ""
    
    # Offer to open
    Write-Host "Preview resources.html in browser? (Y/N): " -ForegroundColor Cyan -NoNewline
    $response = Read-Host
    if ($response -eq 'Y' -or $response -eq 'y') {
        $resourcesPath = Join-Path $scriptPath "resources.html"
        Start-Process $resourcesPath
    }
    
} else {
    Write-Host ""
    Write-Host "Generation encountered errors" -ForegroundColor Red
    Write-Host "Check fora_resources_generator.log for details" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
