# Google Form Setup Guide for Contact Submissions

## Overview
This guide will help you create a Google Form that captures contact submissions from your website and automatically syncs newsletter opt-ins with Mailchimp.

## Step 1: Create the Google Form

1. Go to [https://forms.google.com](https://forms.google.com)
2. Click the **+ Blank** button to create a new form
3. Title: **SEAL Enterprises - Contact Form Submissions**
4. Description: **Travel inquiry and newsletter opt-in form**

## Step 2: Add Form Fields

Add the following questions in this order:

### Question 1: Name
- Type: **Short answer**
- Question: **Full Name**
- Required: **Yes**

### Question 2: Email
- Type: **Short answer**
- Question: **Email Address**
- Required: **Yes**
- Click the three dots (⋮) → Response validation
  - Select: **Text** → **Email**
  - This ensures valid email format

### Question 3: Phone
- Type: **Short answer**
- Question: **Phone Number**
- Required: **No** (optional)

### Question 4: Group Type
- Type: **Dropdown**
- Question: **Who are you traveling with?**
- Required: **No**
- Options:
  - Solo Traveler
  - Couple
  - Family
  - Friends
  - Group/Organization
  - Other

### Question 5: Travel Dates
- Type: **Short answer**
- Question: **Preferred Travel Dates (or flexibility)**
- Required: **No**
- Help text: *Example: June 2026 or Summer 2026*

### Question 6: Budget
- Type: **Short answer**
- Question: **Budget Per Person (optional)**
- Required: **No**
- Help text: *Example: $3,000-$5,000*

### Question 7: Message
- Type: **Paragraph**
- Question: **Tell us about your travel plans and interests**
- Required: **Yes**

### Question 8: Newsletter Opt-In (IMPORTANT!)
- Type: **Checkboxes**
- Question: **Stay Connected**
- Required: **No**
- Options:
  - **Yes, I'd like to receive GPa's Groundings newsletter with travel tips and destination guides**
- Help text: *You can unsubscribe at any time*

## Step 3: Configure Form Settings

1. Click the **Settings** gear icon (⚙️) at top right
2. Under **General** tab:
   - ✓ Collect email addresses (checkbox enabled)
   - ✓ Response receipts: **Respondents can request**
   - ✓ Limit to 1 response (optional - prevents duplicate submissions)
3. Under **Presentation** tab:
   - ✓ Show progress bar
   - Confirmation message: **Thank you! We'll be in touch soon to discuss your travel plans.**
4. Click **Save**

## Step 4: Connect to Google Sheets

1. Click the **Responses** tab at top
2. Click the green **Google Sheets** icon
3. Select **Create a new spreadsheet**
4. Name it: **SEAL Contact Form Responses**
5. Click **Create**

This will automatically create a Google Sheet that captures all form submissions in real-time.

## Step 5: Configure the Spreadsheet

Your Google Sheet will have these columns automatically:
- Timestamp
- Email Address (from form setting)
- Full Name
- Email Address (from question - may be duplicate, that's OK)
- Phone Number
- Who are you traveling with?
- Preferred Travel Dates
- Budget Per Person
- Tell us about your travel plans and interests
- Stay Connected

## Step 6: Export CSV for Mailchimp Sync

When you're ready to sync with Mailchimp:

1. Open your **SEAL Contact Form Responses** Google Sheet
2. Click **File** → **Download** → **Comma Separated Values (.csv)**
3. Save as: **contact_submissions.csv**
4. Move the file to your V1-play folder: `C:\Users\grego\Documents\SEAL Enterprises\Website Code\seal-site\V1-play\`
5. Run the sync tool:
   ```powershell
   .venv\Scripts\python.exe sync_mailchimp_list.py
   ```

## Step 7: Integrate Form with Your Website

You have two options:

### Option A: Embed the Google Form (Easiest)

1. In your Google Form, click **Send** button (top right)
2. Click the **< >** (embed) icon
3. Copy the iframe code
4. Replace the current form in contact.html with this iframe

### Option B: Use Form Submit Redirect (Better UX)

1. In your Google Form, click **Send** → **Link** icon
2. Shorten URL: ✓ (checkbox)
3. Copy the shortened URL
4. In contact.html, change the form action:
   ```html
   <form action="YOUR_GOOGLE_FORM_URL" method="GET">
   ```
5. Update input names to match Google Form entry IDs

To find entry IDs:
1. Open your Google Form in edit mode
2. Right-click on a field → **Inspect**
3. Look for `entry.XXXXXXXXX` in the HTML
4. Match these IDs to your contact.html form fields

### Option C: Use Google Apps Script (Advanced - See GOOGLE_APPS_SCRIPT_SETUP.md)

This allows you to keep your current contact.html form design while posting data to Google Sheets.

## Step 8: Test the Integration

1. Submit a test form with newsletter opt-in checked
2. Verify it appears in your Google Sheet
3. Export CSV and run sync tool
4. Verify the subscriber was added to Mailchimp with "Website Contact Form" tag

## Step 9: Regular Maintenance Workflow

**Weekly or after receiving new submissions:**

1. Open Google Sheet
2. File → Download → CSV
3. Save as contact_submissions.csv in V1-play folder
4. Run sync tool: `.venv\Scripts\python.exe sync_mailchimp_list.py`
5. Review new additions and confirm sync

## CSV Format Expected by Sync Tool

The sync tool expects these column names (will auto-detect variations):
- **email** or **Email Address**
- **name** or **Full Name**
- **phone** or **Phone Number**
- **subscribe-newsletter** or **Stay Connected**
- **timestamp** or **Timestamp**

The tool looks for newsletter opt-in in the "Stay Connected" column. Any response containing "Yes" will be flagged as opt-in.

## Troubleshooting

### Issue: CSV columns don't match
**Solution:** The sync tool is flexible with column names. It will find email, name, and newsletter opt-in columns automatically. If needed, you can rename columns in the Google Sheet before exporting.

### Issue: Newsletter opt-in not detected
**Solution:** Make sure the "Stay Connected" column contains the exact text from your checkbox option: "Yes, I'd like to receive GPa's Groundings newsletter with travel tips and destination guides"

### Issue: Duplicate emails
**Solution:** The sync tool checks if emails already exist in Mailchimp before adding. Duplicates will be skipped.

### Issue: Form submissions not appearing in Sheet
**Solution:** Check that the Google Form is properly linked to the Sheet. Go to Responses tab → three dots (⋮) → Select response destination.

## Next Steps

1. ✅ Create Google Form following this guide
2. ✅ Link to Google Sheets
3. ✅ Test submission flow
4. ✅ Integrate with website (choose Option A, B, or C)
5. ✅ Export first CSV and test sync tool
6. ✅ Add to regular workflow (weekly syncs)

## Files Involved

- `contact.html` - Your website contact form (current design)
- `sync_mailchimp_list.py` - Syncs CSV to Mailchimp
- `contact_submissions.csv` - Exported from Google Sheets
- `mailchimp_config.txt` - Mailchimp credentials
- **Google Form** - (URL to be added after creation)
- **Google Sheet** - (URL to be added after creation)

## Form and Sheet URLs

Once created, add your URLs here for reference:

- **Google Form URL:** _______________________________________________
- **Google Form Edit URL:** _______________________________________________
- **Google Sheet URL:** _______________________________________________

---

**Need Help?** If you encounter issues:
1. Check that column names match between CSV and sync tool expectations
2. Verify email format is valid
3. Ensure opt-in checkbox text is captured correctly
4. Test with a single submission before bulk sync
