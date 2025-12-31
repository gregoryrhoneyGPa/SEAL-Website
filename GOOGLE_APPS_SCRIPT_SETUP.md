# Google Apps Script Setup for Contact Form

## Overview
This approach lets you keep your beautiful contact.html form design while posting data directly to Google Sheets via a custom API endpoint.

## Benefits
- ✅ Keep your existing form design
- ✅ No iframe embedding needed
- ✅ Professional user experience
- ✅ Automatic email notifications
- ✅ CORS-enabled for cross-origin requests

## Step 1: Create Google Sheet

1. Go to [https://sheets.google.com](https://sheets.google.com)
2. Create a new sheet: **SEAL Contact Form Responses**
3. Set up headers in Row 1:
   - A1: `Timestamp`
   - B1: `Name`
   - C1: `Email`
   - D1: `Phone`
   - E1: `Group Type`
   - F1: `Travel Dates`
   - G1: `Budget`
   - H1: `Message`
   - I1: `Newsletter Opt-In`

## Step 2: Open Apps Script Editor

1. In your Google Sheet, click **Extensions** → **Apps Script**
2. Delete any default code
3. Copy and paste the script below

## Step 3: Apps Script Code

```javascript
function doPost(e) {
  try {
    // Get the active spreadsheet
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Parse the POST data
    var data = JSON.parse(e.postData.contents);
    
    // Create timestamp
    var timestamp = new Date();
    
    // Extract form data
    var name = data.name || '';
    var email = data.email || '';
    var phone = data.phone || '';
    var groupType = data['group-type'] || '';
    var dates = data.dates || '';
    var budget = data.budget || '';
    var message = data.message || '';
    var newsletter = data['subscribe-newsletter'] === 'yes' ? 'Yes, I\'d like to receive GPa\'s Groundings newsletter' : 'No';
    
    // Append row to sheet
    sheet.appendRow([
      timestamp,
      name,
      email,
      phone,
      groupType,
      dates,
      budget,
      message,
      newsletter
    ]);
    
    // Optional: Send email notification to you
    var emailBody = 'New contact form submission:\n\n' +
                   'Name: ' + name + '\n' +
                   'Email: ' + email + '\n' +
                   'Phone: ' + phone + '\n' +
                   'Group Type: ' + groupType + '\n' +
                   'Travel Dates: ' + dates + '\n' +
                   'Budget: ' + budget + '\n' +
                   'Message: ' + message + '\n' +
                   'Newsletter Opt-In: ' + newsletter;
    
    MailApp.sendEmail({
      to: 'gregory.rhoney@fora.travel',
      subject: 'New SEAL Enterprises Contact Form Submission',
      body: emailBody
    });
    
    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({
        'status': 'success',
        'message': 'Form submitted successfully'
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    // Return error response
    return ContentService
      .createTextOutput(JSON.stringify({
        'status': 'error',
        'message': error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Test function (optional)
function testDoPost() {
  var testData = {
    postData: {
      contents: JSON.stringify({
        name: 'Test User',
        email: 'test@example.com',
        phone: '555-1234',
        'group-type': 'Couple',
        dates: 'June 2026',
        budget: '$5000',
        message: 'Test message',
        'subscribe-newsletter': 'yes'
      })
    }
  };
  
  var result = doPost(testData);
  Logger.log(result.getContent());
}
```

## Step 4: Deploy as Web App

1. Click **Deploy** → **New deployment**
2. Click the gear icon ⚙️ next to "Select type"
3. Choose **Web app**
4. Configure:
   - **Description:** Contact Form Handler
   - **Execute as:** Me (your email)
   - **Who has access:** Anyone
5. Click **Deploy**
6. Review permissions:
   - Click **Authorize access**
   - Choose your Google account
   - Click **Advanced** → **Go to [Project Name] (unsafe)**
   - Click **Allow**
7. Copy the **Web app URL** (looks like: `https://script.google.com/macros/s/XXXXXXXXXX/exec`)
8. Click **Done**

## Step 5: Update contact.html

Update the form submission JavaScript in contact.html:

```javascript
// Replace the fetch URL with your Web App URL
const FORM_ENDPOINT = 'YOUR_WEB_APP_URL_HERE';

document.querySelector('form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        'group-type': document.getElementById('group-type').value,
        dates: document.getElementById('dates').value,
        budget: document.getElementById('budget').value,
        message: document.getElementById('message').value,
        'subscribe-newsletter': document.getElementById('subscribe-newsletter').checked ? 'yes' : 'no'
    };
    
    try {
        const response = await fetch(FORM_ENDPOINT, {
            method: 'POST',
            mode: 'no-cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        // Show success message
        alert('Thank you! We\'ll be in touch soon to discuss your travel plans.');
        
        // Reset form
        this.reset();
        
    } catch (error) {
        console.error('Error:', error);
        alert('There was an error submitting the form. Please try again or email us directly.');
    }
});
```

## Step 6: Test the Integration

1. Open contact.html in your browser
2. Fill out the form with test data
3. Check "Yes, I'd like to receive GPa's Groundings newsletter"
4. Submit
5. Verify:
   - ✅ Row appears in Google Sheet
   - ✅ Email notification received at gregory.rhoney@fora.travel
   - ✅ Newsletter opt-in captured correctly

## Step 7: Export CSV for Mailchimp Sync

Same process as standard Google Form:

1. Open Google Sheet
2. File → Download → CSV
3. Save as `contact_submissions.csv` in V1-play folder
4. Run: `.venv\Scripts\python.exe sync_mailchimp_list.py`

## Troubleshooting

### Issue: CORS errors in browser console
**Solution:** Use `mode: 'no-cors'` in fetch request (already included above)

### Issue: Script execution failed
**Solution:** 
1. Go to Apps Script editor
2. Click **Run** → **testDoPost** to test
3. Check **Execution log** for errors
4. Verify permissions are granted

### Issue: Email notifications not sending
**Solution:** 
1. Check spam folder
2. Verify MailApp.sendEmail has correct email address
3. Run testDoPost() function to check for errors

### Issue: Data not appearing in Sheet
**Solution:**
1. Check that sheet headers match exactly (Row 1)
2. Verify Web App is deployed as "Execute as: Me"
3. Check "Who has access" is set to "Anyone"

### Issue: Form submission shows error
**Solution:**
1. Open browser DevTools (F12) → Console tab
2. Look for error messages
3. Verify FORM_ENDPOINT URL is correct
4. Test the Web App URL directly in browser

## Advanced: Add Data Validation

In your Google Sheet, you can add validation:

1. Select Email column (C)
2. Data → Data validation
3. Criteria: Text contains "@"
4. On invalid data: Reject input

## Update Web App

If you modify the Apps Script code:

1. Make your changes
2. Click **Deploy** → **Manage deployments**
3. Click the pencil icon ✏️ next to your deployment
4. Change **Version** to **New version**
5. Click **Deploy**
6. URL stays the same (no need to update contact.html)

## Advantages Over Standard Google Form

| Feature | Google Form | Apps Script |
|---------|-------------|-------------|
| Custom design | ❌ Limited | ✅ Full control |
| Branding | ❌ Google branded | ✅ Your brand |
| User experience | ⚠️ Redirect | ✅ Seamless |
| Email notifications | ✅ Yes | ✅ Yes (custom) |
| Data validation | ✅ Yes | ✅ Yes (custom) |
| Setup complexity | ✅ Easy | ⚠️ Moderate |

## Security Notes

- The Web App URL is public but doesn't expose your sheet
- Anyone can POST data to it (intended for form submissions)
- Add rate limiting if you get spam (Apps Script supports quotas)
- Consider adding honeypot field to prevent bots

## Files to Update

1. **contact.html** - Update JavaScript with Web App URL
2. **Google Sheet** - SEAL Contact Form Responses
3. **Apps Script** - Deployed as Web App

---

**Your Web App URL:** _______________________________________________

**Your Google Sheet URL:** _______________________________________________
