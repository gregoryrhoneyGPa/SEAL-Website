Image optimization tool

Usage:

1. From the repository root run:

   npm install
   npm run optimize

2. This reads originals from `images/canva/originals` and writes optimized variants to `images/canva/optimized`.
3. A `report.json` is written to the optimized folder with original and output sizes.

Notes:
- Requires Node.js and `npm` on the system.
- `sharp` will download prebuilt binaries; installation may take a minute.

Run-lighthouse helper

Requires Node.js and npm.

Usage (PowerShell):

.
.\tools\run-lighthouse.ps1 -TargetHost "http://localhost:8000" -OutDir "." -Desktop
or to force Chrome explicitly:

.\tools\run-lighthouse.ps1 -TargetHost "http://localhost:8000" -OutDir "." -Desktop -ChromePath "C:\Program Files\Google\Chrome\Application\chrome.exe"

What it does:
- Uses `npx http-server` to serve the `V1` folder on port 8000 (temporary)
 - Runs `npx lighthouse` against the provided host and writes HTML+JSON outputs to `OutDir`

Notes:
- Running `npx` will download packages if not cached. Ensure Node is installed.
 - If you prefer to serve the site separately, start your server and run the script with `-TargetHost` set accordingly.
 - To force Lighthouse to use Google Chrome instead of Edge, add `-ChromePath` with the full path to `chrome.exe`. The script will also try common install locations if you omit `-ChromePath`.
