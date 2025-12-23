Editing & Testing workflow

Keep changes small, test locally, and use branches.

1) Branch

- Create a branch per change:

  git checkout -b tweak/your-change

2) Edit

- Use VS Code to open and edit files (e.g., `js/main.js`, `Index.html`).
- Prefer small, focused edits. Preserve `prefers-reduced-motion` and UX.

3) Run locally

- Start a simple server from the repo root:

```powershell
# Python
python -m http.server 8000

# or Node (if installed)
npx http-server . -p 8000
```

- Open http://localhost:8000 in your browser and test the change.

4) Validate performance

- Run the existing Lighthouse helper to generate JSONs:

```powershell
.\tools\run-lighthouse.ps1
```

- Inspect the generated `*.json` files in the repo root for before/after metrics.

5) Commit

- Commit small changes with clear messages:

```powershell
git add path/to/changed-file
git commit -m "Describe: what + why"
git push --set-upstream origin tweak/your-change
```

6) Keep history & rollback

- Use `git` to revert or check diffs. Branches and small commits make rollbacks easy.

Tips

- Delay non-critical JS (analytics, autoplay) until idle or after `load` to stabilize LCP.
- Respect `prefers-reduced-motion` and accessibility.
- If you need me to apply consistent changes across demo files, tell me which files and I can patch them.
