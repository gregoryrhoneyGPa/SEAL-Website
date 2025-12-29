# Gmail Integration Setup

## Overview
Form submissions are automatically saved to both:
1. **Excel file**: `docs/contact_submissions.xlsx` (automatic)
2. **Gmail folder**: "SEAL clients" label (requires setup below)

---

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "SEAL Contact Forms" → Click "Create"

---

## Step 2: Enable Gmail API

1. In the Google Cloud Console, search for "Gmail API"
2. Click "Gmail API" → Click "Enable"

---

## Step 3: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** → Select **"OAuth client ID"**
3. If prompted, configure OAuth consent screen:
   - User Type: **External** → Click "Create"
   - App name: **SEAL Contact Forms**
   - User support email: **Your email**
   - Developer email: **Your email**
   - Click **"Save and Continue"** through the rest
4. Back to Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: **SEAL Form Server**
   - Click **"Create"**
5. Download the credentials:
   - Click the **Download** icon (⬇️) next to your OAuth client
   - Save the file as `credentials.json` in this directory:
     ```
     C:\Users\grego\Documents\SEAL Enterprises\Website Code\seal-site\V1-play\
     ```

---

## Step 4: First-Time Authentication

1. Make sure `credentials.json` is in the V1-play folder
2. Start the server:
   ```powershell
   & ".venv\Scripts\python.exe" server.py
   ```
3. A browser window will open asking you to sign in to Google
4. Choose your Gmail account
5. Click **"Allow"** to grant permissions
6. You'll see "The authentication flow has completed"
7. Close the browser tab

The server will save your authentication in `token.json` and you won't need to authenticate again unless the token expires.

---

## Step 5: Test It

1. Start both servers:
   ```powershell
   .\start_servers.ps1
   ```
2. Go to: http://localhost:8000/contact.html
3. Fill out and submit the form
4. Check your Gmail - you should see:
   - A new label: **"SEAL clients"**
   - An email with the form submission

---

## Troubleshooting

### "credentials.json not found"
- Make sure you downloaded the OAuth credentials
- Rename the file to exactly `credentials.json`
- Place it in the same folder as `server.py`

### "Access blocked: This app isn't verified"
This is normal for personal projects:
1. Click "Advanced"
2. Click "Go to SEAL Contact Forms (unsafe)"
3. Click "Allow"

### Token expired
If authentication stops working:
1. Delete `token.json`
2. Restart the server
3. Re-authenticate in the browser

---

## Security Notes

- **Keep `credentials.json` private** - don't share or commit to Git
- **Keep `token.json` private** - it has access to your Gmail
- Add both to `.gitignore`:
  ```
  credentials.json
  token.json
  ```

---

## What Happens When Forms Are Submitted

✅ **With Gmail configured**:
- Saved to Excel: `docs/contact_submissions.xlsx`
- Sent to Gmail with "SEAL clients" label
- Email contains all form data formatted nicely

⚠️ **Without Gmail configured**:
- Still saved to Excel (always works)
- Gmail storage skipped (no error to user)
- Server shows warning message

Both work - Gmail is optional but recommended!
