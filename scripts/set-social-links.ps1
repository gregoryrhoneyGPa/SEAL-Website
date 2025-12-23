$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$index = Join-Path $scriptDir '..\Index.html'
if (-not (Test-Path $index)) { Write-Error "Index.html not found at $index"; exit 2 }
function Ask($prompt,$default){ $v = Read-Host "$prompt [$default]"; if(-not $v){return $default}; return $v }
$fb = Ask 'Facebook URL' '/social/facebook.html'
$insta = Ask 'Instagram URL' '/social/instagram.html'
$linkedin = Ask 'LinkedIn URL' '/social/linkedin.html'

$content = Get-Content $index -Raw -Encoding UTF8
$content = $content -replace 'href="[^"]*facebook[^"]*"','href="' + $fb + '"'
$content = $content -replace 'href="[^"]*instagram[^"]*"','href="' + $insta + '"'
$content = $content -replace 'href="[^"]*linkedin[^"]*"','href="' + $linkedin + '"'
Set-Content $index $content -Encoding UTF8
Write-Host "Updated Index.html social links to:`n Facebook: $fb`n Instagram: $insta`n LinkedIn: $linkedin"
