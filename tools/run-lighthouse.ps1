Param(
  [string]$TargetHost = "http://localhost:8000",
  [string]$OutDir = ".",
  [switch]$Desktop,
  [string]$ChromePath
)

Write-Output "Serving ./ via http-server on port 8000 (if not already running) and running Lighthouse against $TargetHost"

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
# Use cmd.exe /c to run npx (npx is a Node script; calling via cmd avoids Win32 start errors)
Start-Process -FilePath "cmd.exe" -ArgumentList '/c', 'npx', 'http-server', '-p', '8000', './' -WindowStyle Hidden
Start-Sleep -Seconds 2

Write-Output "Running Lighthouse..."

# Auto-detect Chrome path if not provided (common install locations)
if (-not $ChromePath -or $ChromePath -eq "") {
  $common = @(
    'C:\Program Files\Google\Chrome\Application\chrome.exe',
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
    'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
  )
  foreach ($p in $common) {
    if (Test-Path $p) { $ChromePath = $p; break }
  }
}

# Build argument array to avoid quoting issues
$lhArgsArr = @('/c', 'npx', 'lighthouse', $TargetHost, '--output', 'html', '--output', 'json', '--output-path', $outHtml)
if ($preset -ne "") { $lhArgsArr += $preset }

# If we have a Chrome path, instruct Lighthouse to use it
if ($ChromePath -and (Test-Path $ChromePath)) {
  $lhArgsArr += '--chrome-path'
  $lhArgsArr += $ChromePath
  Write-Output "Using Chrome at: $ChromePath"
} else {
  Write-Output "No explicit Chrome path found; Lighthouse will choose a Chromium browser (Edge may be used)."
}

# Run lighthouse and wait for completion
Start-Process -FilePath "cmd.exe" -ArgumentList $lhArgsArr -Wait -WindowStyle Hidden

Write-Output "Lighthouse reports written to: $outHtml and $outJson"
Write-Output "Note: stop the http-server started by this script if you don't need it."
