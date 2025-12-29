# Email Notification Setup

## Overview
Form submissions are automatically saved to both:
1. **Excel file**: `docs/contact_submissions.xlsx` (automatic)
2. **Email notifications**: Sent to your FORA and Gmail addresses (requires setup below)

---

## Step 1: Create Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** (left sidebar)
3. Enable **2-Step Verification** if not already enabled
4. Scroll down to **2-Step Verification** section
5. At the bottom, click **App passwords**
6. In the "Select app" dropdown, choose **Mail**
7. In the "Select device" dropdown, choose **Windows Computer**
8. Click **Generate**
9. **Copy the 16-character password** (it will look like: `abcd efgh ijkl mnop`)

---

## Step 2: Create Configuration File

1. In the V1-play folder, create a new file named: `email_config.txt`
2. Add these two lines (replace with your information):

```
EMAIL=gregory.rhoney@gmail.com
APP_PASSWORD=your-16-character-app-password-here
```

**Important:**
- Remove any spaces from the app password (e.g., `abcdefghijklmnop`)
- Do NOT use your regular Gmail password
- Keep this file secure and never commit it to version control

---

## Step 3: Test It

1. Make sure `email_config.txt` is in the V1-play folder
2. Start both servers:
   ```powershell
   .\start_servers.ps1
   ```
3. Go to: http://localhost:8000/contact.html
4. Fill out and submit the form
5. Check **both** email addresses:
   - gregory.rhoney@fora.travel
   - gregory.rhoney@gmail.com

You should receive the same email notification at both addresses!

---

## Troubleshooting

### "Email not configured" message
- Make sure `email_config.txt` exists in the V1-play folder
- Check that the file has both EMAIL= and APP_PASSWORD= lines
- Make sure there are no extra spaces

### "Authentication failed" error
- Verify you're using an **app password**, not your regular password
- Make sure the app password has no spaces
- Try generating a new app password

### Not receiving emails
- Check your spam/junk folders
- Verify the recipient emails in server.py are correct
- Make sure 2-Step Verification is enabled on your Gmail account

### "Less secure app access" error
Gmail no longer supports this. You **must** use an app password with 2-Step Verification enabled.

---

## Security Notes

- The `email_config.txt` file is listed in `.gitignore` to prevent accidental commits
- App passwords are safer than your regular password
- You can revoke app passwords anytime from your Google Account settings
- Each app password is unique to one application

---

## Changing Email Addresses

To send notifications to different addresses, edit this line in `server.py`:

```python
RECIPIENT_EMAILS = ['gregory.rhoney@fora.travel', 'gregory.rhoney@gmail.com']
```

You can add more addresses or change existing ones.
