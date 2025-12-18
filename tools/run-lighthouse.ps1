Param(
  [string]$Host = "http://localhost:8000",
  [string]$OutDir = ".",
  [switch]$Desktop
)

Write-Output "Serving ./ via http-server on port 8000 (if not already running) and running Lighthouse against $Host"

# Start a simple static server if not already available
$serverCmd = "npx http-server -p 8000 ./"

# Recommend running separately if http-server not installed globally
Write-Output "If you don't have http-server installed, this will use npx to run it temporarily."

if ($Desktop) {
  $preset = "--preset=desktop"
} else {
  $preset = ""
}

$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$outHtml = Join-Path $OutDir "lighthouse-$ts.html"
$outJson = Join-Path $OutDir "lighthouse-$ts.json"

Write-Output "Starting http-server (background)..."
Start-Process -NoNewWindow -FilePath "npx" -ArgumentList "http-server -p 8000 ./" -WindowStyle Hidden
Start-Sleep -Seconds 2

Write-Output "Running Lighthouse..."
$lhArgs = "$Host --output html --output json --output-path $outHtml $preset"
# Use npx to run lighthouse so global install isn't required
Start-Process -NoNewWindow -FilePath "npx" -ArgumentList "lighthouse $lhArgs" -Wait

Write-Output "Lighthouse reports written to: $outHtml and $outJson"
Write-Output "Note: stop the http-server started by this script if you don't need it."
