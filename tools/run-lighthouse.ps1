Param(
  [string]$TargetHost = "http://localhost:8000",
  [string]$OutDir = ".",
  [switch]$Desktop,
  [switch]$Headless = $true,
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
try {
  $resolvedOut = (Resolve-Path -LiteralPath $OutDir).Path
} catch {
  $resolvedOut = (Get-Location).Path
}
$outHtml = Join-Path $resolvedOut "lighthouse-$ts.html"
$outJson = Join-Path $resolvedOut "lighthouse-$ts.json"
Write-Output "Resolved OutDir: $resolvedOut"

Write-Output "Starting http-server (background)..."
# Use cmd.exe /c to run npx (npx is a Node script; calling via cmd avoids Win32 start errors)
Start-Process -FilePath "cmd.exe" -ArgumentList '/c', 'npx', 'http-server', '-p', '8000', './' -WindowStyle Hidden -WorkingDirectory (Get-Location)
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
function Build-LhArgs($outputType, $outputPath) {
  $args = @('/c', 'npx', 'lighthouse', $TargetHost, '--output', $outputType, '--output-path', $outputPath)
  if ($preset -ne "") { $args += $preset }
  if ($ChromePath -and (Test-Path $ChromePath)) {
    $args += '--chrome-path'
    $args += $ChromePath
  }
  if ($Headless) {
    $args += '--chrome-flags'
    $args += '--headless=new'
  }
  return $args
}

# Run Lighthouse for HTML
$htmlArgs = Build-LhArgs 'html' $outHtml
if ($ChromePath -and (Test-Path $ChromePath)) { Write-Output "Using Chrome at: $ChromePath" } else { Write-Output "No explicit Chrome path found; Lighthouse will choose a Chromium browser (Edge may be used)." }
# Ensure the child process runs with the OutDir as working directory so relative paths resolve predictably
# Use the resolved absolute output directory as the working directory for child processes
$workDir = $resolvedOut
Start-Process -FilePath 'cmd.exe' -ArgumentList $htmlArgs -Wait -WindowStyle Hidden -WorkingDirectory $workDir

# Run Lighthouse for JSON
$jsonArgs = Build-LhArgs 'json' $outJson
Start-Process -FilePath 'cmd.exe' -ArgumentList $jsonArgs -Wait -WindowStyle Hidden -WorkingDirectory $workDir

Write-Output "Lighthouse reports written to: $outHtml and $outJson"
Write-Output "Note: stop the http-server started by this script if you don't need it."
