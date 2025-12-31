# FORA Travel Guides - Quick Start Guide

## 🚀 Quick Setup (3 Steps)

### Step 1: Export Your Google Sheet

1. Open your FORA Google Sheet: https://docs.google.com/spreadsheets/d/1ub19wcmOEBmD82Gr05Qw_0Zmn5klXtxxy6ZOBxhyqmQ/edit
2. Click **File → Download → Comma Separated Values (.csv)**
3. Save it as **`fora_guides.csv`** in your V1-play folder
4. Move/rename the downloaded file to: `C:\Users\grego\Documents\SEAL Enterprises\Website Code\seal-site\V1-play\fora_guides.csv`

### Step 2: Run the Automation

```powershell
# Activate your virtual environment (if not already active)
.\.venv\Scripts\Activate.ps1

# Run the automation
python fora_google_sheets_automation.py
```

### Step 3: View Your Travel Guides

Check the newly created **`travel-guides`** folder:
- Individual HTML files for each guide
- `index.json` with all guide metadata

---

## 📁 What Gets Created

```
travel-guides/
├── index.json                    # Catalog of all guides
├── italian-amalfi-coast.html    # Example guide 1
├── paris-france-getaway.html    # Example guide 2
└── caribbean-cruising.html      # Example guide 3
```

Each guide is a **complete, branded HTML page** with:
- ✓ SEAL Enterprises branding
- ✓ FORA Travel attribution
- ✓ Your contact information
- ✓ Mobile-responsive design
- ✓ SEO-optimized structure

---

## 🔄 Regular Updates

### Quick Update Process:
1. **Export** updated CSV from Google Sheets (whenever FORA adds new guides)
2. **Run** `python fora_google_sheets_automation.py`
3. **Done** - Only new guides are published (no duplicates!)

### Automate It:
```powershell
# Create a scheduled task to remind you weekly
.\schedule_fora_automation.ps1
```

Or manually run whenever you want to check for new guides.

---

## 🌐 Add to Your Website

### Option 1: Dynamic Widget (Recommended)

Add to your [index.html](index.html) or [resources.htm](resources.htm):

```html
<!-- Add before closing </body> tag -->
<section class="container" style="margin: 3rem auto;">
  <h2>Free Travel Guides</h2>
  <p>Expert destination guides from SEAL Enterprises</p>
  <div id="travel-guides-widget" data-travel-guides data-layout="grid" data-max-guides="6"></div>
</section>

<script src="dynamic_guides_widget.js"></script>
```

### Option 2: Manual Links

After running automation, add links to specific guides:

```html
<ul>
  <li><a href="travel-guides/italian-amalfi-coast.html">Italian Amalfi Coast Guide</a></li>
  <li><a href="travel-guides/paris-france-getaway.html">Paris France Getaway</a></li>
</ul>
```

---

## 📊 Understanding the Data

Your Google Sheet columns mapped to the website:

| Google Sheet Column | Used For |
|---------------------|----------|
| **Name** | Page title & filename |
| **Description** | Page subtitle & meta description |
| **Magic Content** | Main guide content (THE KEY COLUMN!) |
| **Country, Region, Continent** | Location display |
| **Style, Season** | Tags/categories |
| **< $500 option(s)** | Budget-friendly badge |
| **Partner** | Attribution in tags |

**Note:** Only rows with content in "Magic Content" column are processed.

---

## 🛠 Customization

### Change Output Folder
Edit in script or create `fora_guides_config.txt`:
```
OUTPUT_DIR=my-travel-guides
```

### Change Input CSV Name
```
INPUT_CSV=my-fora-export.csv
```

### Customize HTML Template
Edit the `_create_html_page()` method in `fora_google_sheets_automation.py` to:
- Change colors/styling
- Modify layout
- Add/remove sections
- Update branding

---

## 📝 Logs & Tracking

### View Activity Log:
```powershell
Get-Content fora_guides_automation.log -Tail 30
```

### Check Published State:
```powershell
Get-Content published_guides_state.json
```

This tracks which guides have been published to prevent duplicates.

---

## ❓ Troubleshooting

### "CSV file not found"
Make sure you exported from Google Sheets and saved as `fora_guides.csv` in the V1-play folder.

### "No guides found"
Check that your CSV has:
- A header row with column names
- At least one row with data in the "Magic Content" column

### Guides aren't showing on website
1. Make sure `travel-guides` folder is in your V1-play directory
2. Check that HTML files exist in that folder
3. Verify your website can access the folder (check file paths in HTML)

### Want to republish a guide
Delete its name from `published_guides_state.json` and run the automation again.

### Fresh start
Delete these files to reset:
```powershell
Remove-Item published_guides_state.json
Remove-Item travel-guides -Recurse
```

Then run automation again to republish everything.

---

## 🎯 Next Steps

1. **Test It:** Export CSV and run once to see output
2. **Review:** Check the generated HTML files
3. **Customize:** Adjust styling/branding if needed
4. **Integrate:** Add widget to your website
5. **Schedule:** Set up regular updates (weekly/monthly)

---

## 🔒 Security Notes

- **Don't commit** `fora_guides.csv` to version control (contains FORA content)
- Add to `.gitignore`:
  ```
  fora_guides.csv
  published_guides_state.json
  fora_guides_automation.log
  ```

---

## 💡 Pro Tips

1. **Keep CSV Updated:** Export fresh CSV weekly to get new FORA guides
2. **Backup Published Guides:** Keep your `travel-guides` folder backed up
3. **Monitor Logs:** Check logs occasionally for any errors
4. **Test Before Publishing:** Review generated HTML before adding to live site
5. **Organize by Category:** Use the Style/Season fields to create filtered views

---

## 📞 Quick Commands Reference

```powershell
# Run automation
python fora_google_sheets_automation.py

# View recent logs
Get-Content fora_guides_automation.log -Tail 20

# Count published guides
(Get-ChildItem travel-guides\*.html).Count

# View guide index
Get-Content travel-guides\index.json | ConvertFrom-Json

# Fresh start (republish all)
Remove-Item published_guides_state.json
python fora_google_sheets_automation.py
```

---

Ready to publish your FORA travel guides? Export that CSV and let's go! 🚀
