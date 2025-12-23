# Generate optimized raster variants from SVG using ImageMagick (magick)
# Usage: PowerShell: ./scripts/generate-logo-variants.ps1

$magick = Get-Command magick -ErrorAction SilentlyContinue
if (-not $magick) {
  Write-Error "ImageMagick 'magick' not found in PATH. Install ImageMagick or use the Windows installer and ensure 'magick' is available.";
  exit 1
}

$base = Join-Path $PSScriptRoot "..\images"
Set-Location $base

$svg = "seal-logo.svg"
$mark = "seal-mark.svg"

# Header sizes (width x height)
$header_w = 280
$header_h = 60
$header_w2 = $header_w * 2
$header_h2 = $header_h * 2

# Footer/mark sizes
$mark_1 = 36
$mark_2 = 72

Write-Output "Generating header PNG/WebP variants from $svg"
magick convert -background none "$svg" -resize ${header_w}x${header_h} "seal-logo-horizontal-280.png"
magick convert -background none "$svg" -resize ${header_w2}x${header_h2} "seal-logo-horizontal-560.png"
magick convert -background none "$svg" -resize ${header_w}x${header_h} "seal-logo-horizontal-280.webp"
magick convert -background none "$svg" -resize ${header_w2}x${header_h2} "seal-logo-horizontal-560.webp"

Write-Output "Generating footer/mark PNG/WebP variants from $mark"
magick convert -background none "$mark" -resize ${mark_1}x${mark_1} "seal-mark-36.png"
magick convert -background none "$mark" -resize ${mark_2}x${mark_2} "seal-mark-72.png"
magick convert -background none "$mark" -resize ${mark_1}x${mark_1} "seal-mark-36.webp"
magick convert -background none "$mark" -resize ${mark_2}x${mark_2} "seal-mark-72.webp"

Write-Output "All variants generated: PNG and WebP in images/"
