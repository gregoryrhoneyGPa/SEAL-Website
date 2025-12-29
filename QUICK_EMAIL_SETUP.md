# Quick Email Setup Guide

## What Changed?

Your contact form now sends **actual email notifications** to both:
- gregory.rhoney@fora.travel
- gregory.rhoney@gmail.com

## Setup Steps (5 minutes)

### 1. Get Gmail App Password

1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification** (if not already on)
3. Scroll down and click **App passwords**
4. Select **Mail** and **Windows Computer**
5. Click **Generate**
6. **Copy the 16-character password**

### 2. Create Configuration File

1. Copy `email_config.txt.template` to `email_config.txt`
2. Edit `email_config.txt`:
   - Replace `your-app-password-here` with your app password
   - Remove all spaces from the app password
3. Save the file

### 3. Test It

Run the test script:
```powershell
& .venv\Scripts\python.exe test_email_setup.py
```

You should receive a test email at both addresses!

### 4. Start Your Servers

```powershell
.\start_servers.ps1
```

## Done! 

Now whenever someone submits the contact form:
- ✅ Data saved to Excel spreadsheet
- ✅ Email sent to both your addresses

---

See EMAIL_SETUP.md for detailed instructions and troubleshooting.
