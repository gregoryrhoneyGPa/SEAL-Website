$l = netstat -ano | Select-String ':8000'
if ($l) {
  $p = ($l -split '\s+')[-1]
  try {
    Stop-Process -Id ([int]$p) -Force -ErrorAction Stop
    Write-Output ("Stopped PID " + $p)
  } catch {
    Write-Output ('Failed to stop PID ' + $p + ': ' + $_.ToString())
  }
} else {
  Write-Output 'No listener on port 8000'
}
