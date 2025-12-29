# Contact Form Server Setup

## Overview
The "Plan My Journey" button leads to the contact form which now saves submissions to **TWO locations**:
1. **Excel spreadsheet**: `docs/contact_submissions.xlsx` (automatic)
2. **Gmail**: "SEAL clients" label/folder (requires one-time setup)

## Quick Start

### Without Gmail (Excel Only)
Just run the server - Excel storage works automatically:
```powershell
.\start_servers.ps1
```

### With Gmail (Recommended)
1. Follow the setup in [GMAIL_SETUP.md](GMAIL_SETUP.md) (one-time, ~5 minutes)
2. Run the servers:
```powershell
.\start_servers.ps1
```

## Files Created/Modified
- `server.py` - Flask backend that handles form submissions
- `contact.html` - Updated form with submission handling
- `docs/contact_submissions.xlsx` - Excel file (auto-created)
- `GMAIL_SETUP.md` - Gmail integration instructions
- `start_servers.ps1` - Script to start both servers

## Manual Server Start

### Start Backend Server
```powershell
& ".venv\Scripts\python.exe" server.py
```

### Start Website Server (separate terminal)
```powershell
npx http-server -c-1 . -p 8000
```

## Testing

1. Open: http://localhost:8000/contact.html
2. Fill out the form and submit
3. Check results:
   - **Excel**: Open `docs/contact_submissions.xlsx`
   - **Gmail**: Check your Gmail for "SEAL clients" label

## Data Collected
Each submission saves:
- Timestamp
- Name
- Email
- Phone
- Group Type (Retirees, Families, Affinity Groups, Incentive Travel)
- Preferred Dates
- Budget Range
- Message/Trip Details

## Gmail Integration Benefits

### Why use Gmail storage?
- ✅ **Searchable** - Find submissions quickly
- ✅ **Organized** - All in one dedicated folder
- ✅ **Accessible** - Check from any device
- ✅ **Backed up** - Gmail's automatic backup
- ✅ **Threaded** - Can reply directly to client emails
- ✅ **Shareable** - Easy to forward to team members

### Excel vs Gmail
- **Excel**: Great for spreadsheet analysis, bulk exports
- **Gmail**: Great for daily workflow, email responses

Both formats complement each other!

## Notes
- The backend server must be running for forms to work
- Excel storage always works (no configuration needed)
- Gmail storage is optional but highly recommended
- First Gmail authentication opens a browser window
- Subsequent runs are automatic (token is saved)

## Troubleshooting

### Form not submitting
- Make sure server.py is running (check terminal)
- Verify you're using http://localhost:8000 (not file://)

### Gmail not working
- Excel still saves data normally
- See [GMAIL_SETUP.md](GMAIL_SETUP.md) for configuration
- Check server terminal for error messages

### Need to re-authenticate Gmail
- Delete `token.json`
- Restart server - browser will open for re-auth
