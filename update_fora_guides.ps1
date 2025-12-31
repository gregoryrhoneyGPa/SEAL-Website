# Quick Update Script for FORA Travel Guides
# Run this whenever you export a fresh CSV from Google Sheets

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$csvFile = Join-Path $scriptPath "fora_guides.csv"
$venvPython = Join-Path $scriptPath ".venv\Scripts\python.exe"
$automationScript = Join-Path $scriptPath "fora_google_sheets_automation.py"

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     FORA Travel Guides - Quick Update Tool          ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if CSV exists
if (-not (Test-Path $csvFile)) {
    Write-Host "❌ CSV file not found: $csvFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 Please export your FORA Google Sheet:" -ForegroundColor Yellow
    Write-Host "   1. Open: https://docs.google.com/spreadsheets/d/1ub19wcmOEBmD82Gr05Qw_0Zmn5klXtxxy6ZOBxhyqmQ/edit" -ForegroundColor White
    Write-Host "   2. Click: File → Download → CSV (.csv)" -ForegroundColor White
    Write-Host "   3. Save as: fora_guides.csv" -ForegroundColor White
    Write-Host "   4. Move to: $scriptPath" -ForegroundColor White
    Write-Host ""
    
    # Offer to open download folder
    Write-Host "Open Downloads folder? (Y/N): " -ForegroundColor Cyan -NoNewline
    $response = Read-Host
    if ($response -eq 'Y' -or $response -eq 'y') {
        explorer "$env:USERPROFILE\Downloads"
    }
    
    exit 1
}

# Check CSV file age
$csvAge = (Get-Item $csvFile).LastWriteTime
$ageHours = ((Get-Date) - $csvAge).TotalHours

Write-Host "📄 CSV File: " -ForegroundColor Green -NoNewline
Write-Host "fora_guides.csv" -ForegroundColor White
Write-Host "📅 Last Updated: " -ForegroundColor Green -NoNewline
Write-Host "$csvAge" -ForegroundColor White
Write-Host "⏱️  Age: " -ForegroundColor Green -NoNewline

if ($ageHours -lt 1) {
    Write-Host "$([Math]::Round($ageHours * 60)) minutes ago" -ForegroundColor Green
} elseif ($ageHours -lt 24) {
    Write-Host "$([Math]::Round($ageHours)) hours ago" -ForegroundColor Yellow
} else {
    Write-Host "$([Math]::Round($ageHours / 24)) days ago" -ForegroundColor Red
    Write-Host ""
    Write-Host "⚠️  CSV is older than 24 hours. Consider exporting a fresh copy." -ForegroundColor Yellow
}

Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path $venvPython)) {
    Write-Host "❌ Python virtual environment not found" -ForegroundColor Red
    Write-Host "Expected at: $venvPython" -ForegroundColor Yellow
    exit 1
}

# Run the automation
Write-Host "🚀 Running automation..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

& $venvPython $automationScript

$exitCode = $LASTEXITCODE

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

if ($exitCode -eq 0) {
    Write-Host ""
    Write-Host "✅ Update complete!" -ForegroundColor Green
    Write-Host ""
    
    # Show stats
    $guidesDir = Join-Path $scriptPath "travel-guides"
    if (Test-Path $guidesDir) {
        $guideCount = (Get-ChildItem "$guidesDir\*.html" -ErrorAction SilentlyContinue).Count
        Write-Host "📚 Total Guides Published: $guideCount" -ForegroundColor Cyan
        
        $indexFile = Join-Path $guidesDir "index.json"
        if (Test-Path $indexFile) {
            Write-Host "📄 View catalog: travel-guides\index.json" -ForegroundColor White
        }
    }
    
    Write-Host ""
    Write-Host "📁 Output folder: $guidesDir" -ForegroundColor White
    Write-Host ""
    
    # Offer to open folder
    Write-Host "Open travel-guides folder? (Y/N): " -ForegroundColor Cyan -NoNewline
    $response = Read-Host
    if ($response -eq 'Y' -or $response -eq 'y') {
        explorer $guidesDir
    }
    
} else {
    Write-Host ""
    Write-Host "❌ Automation encountered errors" -ForegroundColor Red
    Write-Host "Check fora_guides_automation.log for details" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
