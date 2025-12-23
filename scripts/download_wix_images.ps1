<#
Robust downloader for Wix/static image URLs found in a saved HTML file.
Usage (PowerShell):
  powershell -ExecutionPolicy Bypass -File .\V1\scripts\download_wix_images.ps1
#>

Param(
  [string]$LiveHtml = "c:\\Users\\grego\\Documents\\SEAL Enterprises\\Website Code\\seal-site\\V1\\live-seal-home.html",
  [string]$OutDir = "c:\\Users\\grego\\Documents\\SEAL Enterprises\\Website Code\\seal-site\\V1\\images",
  [switch]$VerboseMode
)

if (-not (Test-Path $LiveHtml)) { Write-Error "Live HTML not found: $LiveHtml"; exit 1 }
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

# Match only common image file extensions and typical Wix/media hosts
$pattern = '(https?://(?:static\.wixstatic\.com|static\.parastorage\.com|filesusr\.com|siteassets\.parastorage\.com)[^"''\s>]*?\.(?:png|jpe?g|gif|svg|webp|avif|ico))(?:\?[^"''\s>]*)?'

$html = Get-Content -Raw -Path $LiveHtml -ErrorAction Stop

$matches = [regex]::Matches($html, $pattern, 'IgnoreCase') | ForEach-Object { $_.Groups[1].Value }
$urls = $matches | Select-Object -Unique

if ($urls.Count -eq 0) { Write-Host "No image URLs found by pattern."; exit 0 }

Write-Host "Found $($urls.Count) unique image URLs. Starting downloads to: $OutDir"

foreach ($url in $urls) {
  try {
    # sanitize URL (trim closing script/text fragments that sometimes get captured)
    $url = $url.TrimEnd('"','\'','>')

    # derive file name and sanitize illegal filename chars
    $fileName = [System.IO.Path]::GetFileName(($url -split '\?')[0])
    if ([string]::IsNullOrWhiteSpace($fileName)) { $fileName = "image_$([guid]::NewGuid().ToString()).bin" }
    $fileName = $fileName -replace '[\[\]\\/:*?"<>|]', '-'

    $out = Join-Path $OutDir $fileName
    if (Test-Path $out) { Write-Host "Skipping (exists): $fileName"; continue }

    Write-Host "Downloading $url -> $out"
    Invoke-WebRequest -Uri $url -OutFile $out -ErrorAction Stop
    Start-Sleep -Milliseconds 150
  }
  catch {
    Write-Warning "Failed: $url — $($_.Exception.Message)"
  }
}

Write-Host "Done. Check $OutDir for downloaded images. Note: some protected endpoints may return AccessDenied and are skipped."