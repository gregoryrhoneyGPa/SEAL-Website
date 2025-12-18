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
