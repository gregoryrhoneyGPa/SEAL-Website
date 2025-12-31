# Quick PDF Conversion Script
# Converts FORA PDF travel guides to website HTML pages

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $scriptPath ".venv\Scripts\python.exe"
$conversionScript = Join-Path $scriptPath "fora_pdf_to_web.py"
$pdfDir = "c:\Users\grego\Documents\FORA\Travel Guides"

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   FORA PDF → Website Converter                       ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if PDF directory exists
if (-not (Test-Path $pdfDir)) {
    Write-Host "❌ PDF directory not found: $pdfDir" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please create the directory and add your FORA PDF guides." -ForegroundColor Yellow
    exit 1
}

# Count PDFs
$pdfCount = (Get-ChildItem $pdfDir -Filter *.pdf -ErrorAction SilentlyContinue).Count

Write-Host "📁 PDF Directory: " -ForegroundColor Green -NoNewline
Write-Host $pdfDir -ForegroundColor White
Write-Host "📄 PDFs Found: " -ForegroundColor Green -NoNewline
Write-Host "$pdfCount files" -ForegroundColor White
Write-Host ""

if ($pdfCount -eq 0) {
    Write-Host "⚠️  No PDF files found" -ForegroundColor Yellow
    Write-Host "Please add FORA travel guide PDFs to the directory above." -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "Open folder? (Y/N): " -ForegroundColor Cyan -NoNewline
    $response = Read-Host
    if ($response -eq 'Y' -or $response -eq 'y') {
        explorer $pdfDir
    }
    exit 1
}

# Check virtual environment
if (-not (Test-Path $venvPython)) {
    Write-Host "❌ Python virtual environment not found" -ForegroundColor Red
    exit 1
}

# Install PyPDF2 if needed
Write-Host "📦 Checking dependencies..." -ForegroundColor Cyan
& $venvPython -m pip install --quiet PyPDF2

# Run conversion
Write-Host ""
Write-Host "🚀 Starting conversion..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

& $venvPython $conversionScript

$exitCode = $LASTEXITCODE

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

if ($exitCode -eq 0) {
    Write-Host ""
    Write-Host "✅ Conversion complete!" -ForegroundColor Green
    Write-Host ""
    
    # Show stats
    $guidesDir = Join-Path $scriptPath "travel-guides"
    if (Test-Path $guidesDir) {
        $htmlCount = (Get-ChildItem "$guidesDir\*.html" -ErrorAction SilentlyContinue).Count
        $pdfCopyCount = (Get-ChildItem "$guidesDir\*.pdf" -ErrorAction SilentlyContinue).Count
        
        Write-Host "📊 Results:" -ForegroundColor Cyan
        Write-Host "   HTML pages created: $htmlCount" -ForegroundColor White
        Write-Host "   PDFs copied: $pdfCopyCount" -ForegroundColor White
        Write-Host "   Output folder: $guidesDir" -ForegroundColor White
    }
    
    Write-Host ""
    Write-Host "Open travel-guides folder? (Y/N): " -ForegroundColor Cyan -NoNewline
    $response = Read-Host
    if ($response -eq 'Y' -or $response -eq 'y') {
        explorer $guidesDir
    }
    
} else {
    Write-Host ""
    Write-Host "❌ Conversion encountered errors" -ForegroundColor Red
    Write-Host "Check fora_pdf_conversion.log for details" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
