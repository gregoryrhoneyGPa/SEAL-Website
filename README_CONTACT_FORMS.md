# SEAL Contact Form System - Complete Guide

## 📋 System Overview

The "Plan My Journey" button on your SEAL website now collects form submissions and saves them to **two locations**:

1. **📊 Excel Spreadsheet**: `docs/contact_submissions.xlsx`
2. **📧 Gmail Folder**: "SEAL clients" label

Both servers can run **automatically in the background** whenever your computer is on.

---

## 🎯 Quick Start Guides

### First-Time Setup (Choose One)

#### Option A: Automatic Startup (Recommended)
**Servers start when Windows boots, run in background**

1. Open PowerShell as Administrator
2. Navigate to project folder
3. Run: `.\setup_autostart.ps1`
4. Done! Servers now start automatically

📖 Full guide: [AUTOSTART_SETUP.md](AUTOSTART_SETUP.md)

#### Option B: Manual Startup
**Start/stop servers manually when needed**

1. Run: `.\start_servers.ps1`
2. Access form: http://localhost:8000/contact.html
3. Stop when done: `.\stop_servers.ps1`

📖 Full guide: [START_FORM_SERVER.md](START_FORM_SERVER.md)

### Gmail Integration (Optional but Recommended)
**Get form submissions in Gmail**

1. Follow steps in [GMAIL_SETUP.md](GMAIL_SETUP.md) (~5 minutes)
2. One-time Google authentication
3. Forms automatically emailed to "SEAL clients" folder

---

## 📂 File Structure

```
V1-play/
├── server.py                          # Flask backend (handles forms)
├── contact.html                       # Contact form page
├── docs/
│   └── contact_submissions.xlsx       # Excel data storage
│
├── Automatic Startup Scripts:
├── setup_autostart.ps1               # Set up auto-start (run once)
├── remove_autostart.ps1              # Remove auto-start
├── start_servers_background.ps1      # Background launcher
├── stop_servers.ps1                  # Stop all servers
├── check_servers.ps1                 # Check server status
│
├── Manual Startup Scripts:
├── start_servers.ps1                 # Start with visible windows
│
├── Documentation:
├── README_CONTACT_FORMS.md           # This file
├── AUTOSTART_SETUP.md                # Automatic startup guide
├── START_FORM_SERVER.md              # Manual startup guide
├── GMAIL_SETUP.md                    # Gmail integration guide
│
└── Configuration:
    ├── credentials.json              # Gmail OAuth (you create this)
    └── token.json                    # Gmail auth token (auto-created)
```

---

## 🔄 Common Workflows

### Daily Use (Automatic Mode)
```powershell
# Check if servers are running
.\check_servers.ps1

# Stop servers if needed
.\stop_servers.ps1
```

### Daily Use (Manual Mode)
```powershell
# Start servers
.\start_servers.ps1

# Stop when done
.\stop_servers.ps1
```

### Check New Submissions
- **Excel**: Open `docs/contact_submissions.xlsx`
- **Gmail**: Check "SEAL clients" label in Gmail

### View Logs
```powershell
# Automatic startup logs
Get-Content server_startup.log -Tail 20

# Real-time monitoring
Get-Content server_startup.log -Wait
```

---

## 🌐 Access URLs

### On Your Computer
- **Website**: http://localhost:8000
- **Contact Form**: http://localhost:8000/contact.html
- **API**: http://localhost:5000

### From Other Devices
1. Find your IP:
   ```powershell
   ipconfig
   # Look for IPv4 Address
   ```
2. Use: `http://YOUR-IP:8000/contact.html`

---

## 📊 Data Collection

### Fields Captured
- Timestamp
- Name
- Email
- Phone
- Group Type (Retirees, Families, Affinity Groups, Incentive Travel)
- Preferred Dates
- Budget Range
- Message/Trip Details

### Storage Locations

| Location | Format | Always Available | Searchable | Requires Setup |
|----------|--------|------------------|------------|----------------|
| Excel | Spreadsheet | ✅ Yes | Limited | ❌ None |
| Gmail | Email | ✅ Yes* | ✅ Yes | ✅ One-time |

*Gmail requires internet connection

---

## 🛠️ Management Commands

### Server Status
```powershell
.\check_servers.ps1                    # Check if running
Get-ScheduledTask "SEAL Contact*"      # Check autostart status
```

### Start/Stop
```powershell
.\start_servers.ps1                    # Manual start (visible)
.\start_servers_background.ps1         # Manual start (hidden)
.\stop_servers.ps1                     # Stop all servers
```

### Autostart Management
```powershell
.\setup_autostart.ps1                  # Enable autostart
.\remove_autostart.ps1                 # Disable autostart
```

### View Data
```powershell
# Open Excel file
Invoke-Item "docs\contact_submissions.xlsx"

# Count submissions
(Import-Excel "docs\contact_submissions.xlsx").Count

# View in PowerShell
Import-Excel "docs\contact_submissions.xlsx" | Format-Table
```

---

## 🐛 Troubleshooting

### Servers Won't Start
```powershell
# Check what's using the ports
Get-NetTCPConnection -LocalPort 5000,8000

# Kill conflicting processes
Get-Process python,node | Stop-Process -Force

# Try starting again
.\start_servers.ps1
```

### Form Not Submitting
1. Verify servers are running: `.\check_servers.ps1`
2. Check browser console for errors (F12)
3. Verify URL is http://localhost:8000 (not file://)
4. Review server logs: `Get-Content server_startup.log`

### Gmail Not Working
- Excel storage still works (always functional)
- See [GMAIL_SETUP.md](GMAIL_SETUP.md) for configuration
- Re-authenticate: Delete `token.json`, restart server

### Autostart Not Working
```powershell
# Verify task exists
Get-ScheduledTask "SEAL Contact*"

# Check task history
Get-ScheduledTask "SEAL Contact*" | Get-ScheduledTaskInfo

# Re-run setup
.\setup_autostart.ps1
```

---

## 🔒 Security & Privacy

### Protected Files (Don't Share)
- `credentials.json` - Gmail OAuth credentials
- `token.json` - Gmail access token
- `docs/contact_submissions.xlsx` - Customer data

### Git Safety
These files are in `.gitignore` and won't be committed:
- credentials.json
- token.json
- contact_submissions.xlsx
- Server logs and PIDs

### Best Practices
- ✅ Regular backups of Excel file
- ✅ Keep Gmail credentials secure
- ✅ Use HTTPS in production
- ✅ Review server logs periodically
- ✅ Update Python packages regularly

---

## 📈 Production Deployment

For live website deployment (not localhost):

### Netlify Forms (Alternative)
If hosting on Netlify, you can use built-in forms:
- No server needed
- Automatic spam filtering
- Email notifications
- See: https://docs.netlify.com/forms/setup/

### VPS Deployment
For your own server:
1. Use production WSGI server (Gunicorn)
2. Set up HTTPS (Let's Encrypt)
3. Configure firewall
4. Use process manager (systemd)
5. Regular backups

---

## 🎓 Learning Resources

### PowerShell Basics
- Task Scheduler: `taskschd.msc`
- Process management: `Get-Process`, `Stop-Process`
- Network info: `Get-NetTCPConnection`

### Flask Development
- Official docs: https://flask.palletsprojects.com/
- Production deployment: Use Gunicorn or uWSGI

### Gmail API
- Python quickstart: https://developers.google.com/gmail/api/quickstart/python
- API reference: https://developers.google.com/gmail/api

---

## 📞 Getting Help

### Check Status First
```powershell
.\check_servers.ps1
Get-Content server_startup.log -Tail 50
```

### Common Issues
1. Port conflicts → Change ports in configuration
2. Python not found → Activate virtual environment
3. Node not installed → Install Node.js
4. Gmail errors → Re-run authentication

### Reset Everything
```powershell
.\stop_servers.ps1
Remove-Item token.json -Force
Remove-Item .flask_pid,.http_pid,server_startup.log -Force
.\setup_autostart.ps1
```

---

## ✅ Setup Checklist

- [ ] Python environment configured (`.venv`)
- [ ] Required packages installed (Flask, openpyxl, etc.)
- [ ] Node.js installed (for http-server)
- [ ] Servers tested manually (`.\start_servers.ps1`)
- [ ] Form submission tested (Excel file created)
- [ ] Gmail configured (optional) ([GMAIL_SETUP.md](GMAIL_SETUP.md))
- [ ] Autostart configured (optional) ([AUTOSTART_SETUP.md](AUTOSTART_SETUP.md))
- [ ] Firewall rules added (if accessing remotely)
- [ ] Backup strategy in place

---

## 🎉 You're All Set!

Your contact form system is ready to collect client inquiries automatically!

**Test it now:**
```powershell
.\check_servers.ps1
```

Then visit: **http://localhost:8000/contact.html**

Need help? Check the specific guides:
- 🚀 [AUTOSTART_SETUP.md](AUTOSTART_SETUP.md) - Automatic startup
- 📧 [GMAIL_SETUP.md](GMAIL_SETUP.md) - Gmail integration
- 📖 [START_FORM_SERVER.md](START_FORM_SERVER.md) - Manual operation
