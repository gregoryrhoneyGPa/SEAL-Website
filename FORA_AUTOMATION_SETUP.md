# FORA Travel Guides & Mailchimp Automation Setup

## Overview
This automation system will:
- ✓ Automatically fetch FORA "magic" travel guides
- ✓ Rebrand them with your SEAL branding
- ✓ Publish them to your website
- ✓ Create Mailchimp campaigns (optional)
- ✓ Handle credential re-validation automatically
- ✓ Run on a schedule (daily check for new content)

---

## Step 1: Configure FORA Credentials

1. Copy the template file:
   ```powershell
   Copy-Item fora_config.txt.template fora_config.txt
   ```

2. Edit `fora_config.txt` with your actual credentials:
   - **FORA_USERNAME**: Your FORA login email/username
   - **FORA_PASSWORD**: Your FORA password
   - **FORA_ADVISOR_ID**: Your FORA advisor ID (already set to gregory-rhoney)
   - **FORA URLs**: Update if FORA provides specific portal URLs

---

## Step 2: Configure Mailchimp

### Get Mailchimp API Key
1. Log in to Mailchimp
2. Go to **Account → Extras → API Keys**
3. Create a new API key or copy existing one

### Get List ID
1. In Mailchimp, go to **Audience → All contacts**
2. Click **Settings → Audience name and defaults**
3. Look for **Audience ID** (looks like: `a1b2c3d4e5`)

### Get Server Prefix
- Look at your Mailchimp URL: `https://us21.admin.mailchimp.com/`
- The server prefix is the part before `.admin` (e.g., `us21`)

### Update fora_config.txt:
```
MAILCHIMP_API_KEY=your-actual-api-key-here
MAILCHIMP_SERVER_PREFIX=us21
MAILCHIMP_LIST_ID=your-audience-id-here
```

---

## Step 3: Configure Automation Settings

In `fora_config.txt`, adjust these settings:

```
# How often to check for new guides (in hours)
CHECK_INTERVAL_HOURS=24

# Automatically publish guides to your website?
AUTO_PUBLISH_TO_WEBSITE=True

# Automatically create Mailchimp campaigns? (False = create draft only)
AUTO_SEND_TO_MAILCHIMP=False
```

**Recommended:** Set `AUTO_SEND_TO_MAILCHIMP=False` so campaigns are created as drafts for your review before sending.

---

## Step 4: Install Dependencies

Run this command:
```powershell
.\.venv\Scripts\Activate.ps1
pip install requests beautifulsoup4 mailchimp-marketing lxml
```

---

## Step 5: Test the Automation

### Manual Test Run:
```powershell
python fora_automation.py
```

This will:
1. Validate your credentials
2. Authenticate with FORA
3. Test Mailchimp connection
4. Fetch available travel guides
5. Download and publish new guides
6. Create Mailchimp campaigns (if enabled)

### Check the logs:
```powershell
Get-Content fora_automation.log -Tail 50
```

---

## Step 6: Schedule Automatic Updates

Run the scheduler setup:
```powershell
.\schedule_fora_automation.ps1
```

This creates a Windows scheduled task that runs daily at 9:00 AM.

### Manage the Schedule:
```powershell
# View the task
Get-ScheduledTask -TaskName "FORA_Travel_Automation"

# Run immediately
Start-ScheduledTask -TaskName "FORA_Travel_Automation"

# Disable
Disable-ScheduledTask -TaskName "FORA_Travel_Automation"

# Enable
Enable-ScheduledTask -TaskName "FORA_Travel_Automation"

# Remove
Unregister-ScheduledTask -TaskName "FORA_Travel_Automation"
```

---

## Step 7: Add Travel Guides to Your Website

The automation creates a `travel-guides` folder with:
- Individual guide HTML files
- `index.json` with all guide metadata

### Option A: Display Guides Dynamically

Add this to your `index.html` or create a new `resources.html`:

```html
<section id="travel-guides" class="container" style="margin: 3rem auto;">
  <h2>Free Travel Guides</h2>
  <p>Expert destination guides curated by SEAL Enterprises</p>
  <div id="guides-container" class="guides-grid"></div>
</section>

<script>
// Load and display travel guides
fetch('travel-guides/index.json')
  .then(response => response.json())
  .then(data => {
    const container = document.getElementById('guides-container');
    data.guides.forEach(guide => {
      const card = document.createElement('div');
      card.className = 'guide-card';
      card.innerHTML = `
        <h3>${guide.title}</h3>
        <p>${guide.description}</p>
        <a href="travel-guides/${guide.filename}" class="btn">Read Guide</a>
      `;
      container.appendChild(card);
    });
  });
</script>
```

### Option B: Manual Integration

After automation runs, check `travel-guides/` folder and manually add links to your pages.

---

## Understanding the Workflow

### Daily Automation Cycle:
1. **Authentication Check** (9:00 AM daily)
   - Validates FORA credentials
   - Re-authenticates if needed
   - Alerts if credentials expired

2. **Content Fetch**
   - Scans FORA portal for new "magic" guides
   - Compares with previously published guides
   - Downloads only new content

3. **Website Publishing**
   - Rebrands content with SEAL logo/info
   - Creates individual HTML pages
   - Updates index.json

4. **Mailchimp Integration**
   - Creates campaign draft with guide content
   - Adds to your audience list
   - Waits for your review before sending

5. **State Management**
   - Saves processed guides to `automation_state.json`
   - Prevents duplicate processing
   - Tracks last successful run

---

## Credential Re-validation

The system handles credential expiration automatically:

- **Every 24 hours**: Re-authenticates with FORA
- **On error**: Attempts re-authentication
- **If failed**: Logs error and sends notification

### If credentials expire:
1. Update `fora_config.txt` with new credentials
2. Run: `python fora_automation.py`
3. System will resume automatically

---

## Troubleshooting

### "Configuration file not found"
```powershell
Copy-Item fora_config.txt.template fora_config.txt
# Then edit fora_config.txt with your credentials
```

### "Authentication failed"
- Verify FORA username/password in `fora_config.txt`
- Try logging into FORA website manually to confirm credentials
- Check if FORA changed their login page URL

### "Mailchimp connection failed"
- Verify API key is correct
- Check server prefix matches your Mailchimp URL
- Ensure API key has proper permissions

### "No guides found"
- FORA may have changed their HTML structure
- Check `fora_automation.log` for details
- You may need to provide sample FORA pages for parsing

---

## Customization

### Change Schedule
Edit in `schedule_fora_automation.ps1`:
```powershell
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
# Change to: -Daily -At 2pm
# Or: -Weekly -DaysOfWeek Monday -At 9am
```

### Change Guide Template
Edit `_rebrand_content()` method in `fora_automation.py` to customize:
- HTML structure
- CSS styles
- Branding elements
- Call-to-action buttons

### Add Email Notifications
Modify `fora_automation.py` to send email alerts when:
- New guides are published
- Credentials need renewal
- Errors occur

---

## Files Created

- **fora_config.txt** - Your credentials (keep private!)
- **fora_automation.py** - Main automation script
- **automation_state.json** - Tracking processed guides
- **fora_automation.log** - Detailed activity log
- **travel-guides/** - Published guide HTML files
- **travel-guides/index.json** - Guide metadata

---

## Security Notes

1. **Never commit** `fora_config.txt` to version control
2. Add to `.gitignore`:
   ```
   fora_config.txt
   automation_state.json
   fora_automation.log
   ```

3. Keep API keys secure
4. Use environment variables for production deployments

---

## Next Steps

After setup:
1. Run a manual test
2. Review the generated guides in `travel-guides/`
3. Check Mailchimp for draft campaigns
4. Enable scheduled task
5. Monitor logs for first few runs

---

## Support

If you encounter issues:
1. Check `fora_automation.log`
2. Verify all credentials
3. Test FORA login manually
4. Provide sample FORA guide URLs for parsing refinement
