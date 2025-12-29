# Automatic Startup Configuration

## Overview
Your SEAL contact form servers can now start automatically whenever Windows boots up and run continuously in the background. This ensures form submissions are always captured, even after restarts.

---

## 🚀 Quick Setup (One-Time)

### Step 1: Run Setup Script
Right-click **PowerShell** → Select **"Run as Administrator"**

```powershell
cd "C:\Users\grego\Documents\SEAL Enterprises\Website Code\seal-site\V1-play"
.\setup_autostart.ps1
```

### Step 2: Follow the prompts
- The script will create a Windows Task Scheduler entry
- Choose **"Y"** when asked to start servers now
- That's it! ✅

---

## 📋 What Was Configured

### Windows Task Scheduler Entry
- **Task Name**: "SEAL Contact Form Servers"
- **Trigger**: Runs at Windows startup
- **Action**: Starts both Flask and HTTP servers in background
- **Auto-restart**: If servers crash, they restart automatically
- **User**: Runs as your user account

### Background Servers
Both servers run hidden (no windows):
- **Flask API**: http://localhost:5000 (form submission handler)
- **HTTP Server**: http://localhost:8000 (website)

---

## 🔧 Management Scripts

### Check Server Status
```powershell
.\check_servers.ps1
```
Shows if servers are running and autostart status

### Stop Servers
```powershell
.\stop_servers.ps1
```
Stops both servers immediately

### Start Servers Manually
```powershell
.\start_servers_background.ps1
```
Starts servers in background (without Task Scheduler)

### Disable Autostart
```powershell
.\remove_autostart.ps1
```
Removes the scheduled task (run as Administrator)

---

## 📊 Monitoring

### View Startup Logs
```powershell
Get-Content server_startup.log -Tail 20
```

### Check Task Scheduler
1. Press `Win + R`
2. Type: `taskschd.msc`
3. Look for: "SEAL Contact Form Servers"

### Task Status Commands
```powershell
# Check task status
Get-ScheduledTask -TaskName "SEAL Contact Form Servers"

# Start task manually
Start-ScheduledTask -TaskName "SEAL Contact Form Servers"

# Stop task
Stop-ScheduledTask -TaskName "SEAL Contact Form Servers"
```

---

## 🔄 How It Works

1. **Windows starts** → Task Scheduler triggers
2. **Task runs** → `start_servers_background.ps1` executes
3. **Flask starts** → Backend ready to receive forms
4. **HTTP server starts** → Website accessible
5. **Logging** → Activity logged to `server_startup.log`
6. **Auto-restart** → If crash detected, restarts automatically

---

## 🌐 Accessing Your Site

Once running, access from any device on your network:

### On the same computer
- http://localhost:8000
- http://localhost:8000/contact.html

### From other devices (phone, tablet, etc.)
1. Find your computer's IP address:
   ```powershell
   (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -like "*Wi-Fi*" -or $_.InterfaceAlias -like "*Ethernet*"}).IPAddress
   ```
2. Use that IP: `http://YOUR-IP:8000/contact.html`

---

## ⚠️ Important Notes

### Firewall
If accessing from other devices, you may need to allow traffic:
```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "SEAL HTTP Server" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
New-NetFirewallRule -DisplayName "SEAL Flask API" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
```

### Sleep/Hibernate
- Servers pause when computer sleeps
- Automatically resume when computer wakes
- Use Task Scheduler settings to prevent sleep if needed

### Gmail Integration
- Token persists across reboots
- May need to re-authenticate if token expires (rare)
- Excel storage always works regardless

### Ports
- Flask: Port 5000
- HTTP: Port 8000
- If ports are in use, servers will fail to start (check logs)

---

## 🐛 Troubleshooting

### Servers not starting automatically
```powershell
# Check task exists
Get-ScheduledTask -TaskName "SEAL Contact Form Servers"

# Check task history
Get-ScheduledTask "SEAL Contact Form Servers" | Get-ScheduledTaskInfo

# View logs
Get-Content server_startup.log
```

### Can't access from other devices
- Check Windows Firewall settings
- Verify both computers on same network
- Use computer name: `http://YOUR-PC-NAME:8000`

### Task says "Running" but servers aren't accessible
```powershell
# Stop everything
.\stop_servers.ps1

# Restart task
Start-ScheduledTask -TaskName "SEAL Contact Form Servers"

# Wait 5 seconds
Start-Sleep -Seconds 5

# Check status
.\check_servers.ps1
```

### Need to change ports
Edit [server.py](server.py) (Flask port) and [start_servers_background.ps1](start_servers_background.ps1) (HTTP port)

---

## 🗑️ Complete Removal

To completely remove automatic startup:

```powershell
# Run as Administrator
.\remove_autostart.ps1
.\stop_servers.ps1
```

Or manually in Task Scheduler:
1. Open Task Scheduler (`taskschd.msc`)
2. Find "SEAL Contact Form Servers"
3. Right-click → Delete

---

## 📂 Files Reference

| File | Purpose |
|------|---------|
| `setup_autostart.ps1` | One-time setup (creates scheduled task) |
| `remove_autostart.ps1` | Remove scheduled task |
| `start_servers_background.ps1` | Background server launcher |
| `stop_servers.ps1` | Stop all servers |
| `check_servers.ps1` | Check server status |
| `server_startup.log` | Runtime log file |
| `.flask_pid` | Flask process ID |
| `.http_pid` | HTTP server process ID |

---

## ✅ Verification

After setup, verify everything works:

1. **Check status**: `.\check_servers.ps1`
2. **Test form**: http://localhost:8000/contact.html
3. **Submit test data**: Fill and submit form
4. **Verify Excel**: Check `docs/contact_submissions.xlsx`
5. **Verify Gmail**: Check "SEAL clients" label (if configured)
6. **Reboot test**: Restart computer and verify servers auto-start

---

## 💡 Tips

- Check logs regularly: `Get-Content server_startup.log`
- Status at a glance: `.\check_servers.ps1`
- Before computer maintenance: `.\stop_servers.ps1`
- After maintenance: Servers auto-start on next boot
- Share form link with clients: Use your computer's IP address

Your form collection system is now fully automated! 🎉
