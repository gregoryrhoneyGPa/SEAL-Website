"""
Quick test script to verify email setup is working
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_CONFIG_FILE = 'email_config.txt'
RECIPIENT_EMAILS = ['gregory.rhoney@fora.travel', 'gregory.rhoney@gmail.com']

def load_email_config():
    """Load email configuration from file"""
    if not os.path.exists(EMAIL_CONFIG_FILE):
        return None, None
    
    try:
        with open(EMAIL_CONFIG_FILE, 'r') as f:
            lines = f.readlines()
            email = None
            password = None
            for line in lines:
                line = line.strip()
                if line.startswith('EMAIL='):
                    email = line.split('=', 1)[1]
                elif line.startswith('APP_PASSWORD='):
                    password = line.split('=', 1)[1]
            return email, password
    except Exception as e:
        print(f"Error reading email config: {e}")
        return None, None

def main():
    print("\nEMAIL INTEGRATION CHECK")
    print("="*50)
    
    # Check if config file exists
    if not os.path.exists(EMAIL_CONFIG_FILE):
        print(f"\n❌ {EMAIL_CONFIG_FILE} not found!")
        print(f"   Follow EMAIL_SETUP.md to create this file\n")
        return
    
    print(f"✓ Found {EMAIL_CONFIG_FILE}")
    
    # Load credentials
    sender_email, app_password = load_email_config()
    
    if not sender_email or not app_password:
        print(f"\n❌ Invalid configuration in {EMAIL_CONFIG_FILE}")
        print("   Make sure you have both EMAIL= and APP_PASSWORD= lines\n")
        return
    
    print(f"✓ Email configured: {sender_email}")
    print(f"✓ Recipients: {', '.join(RECIPIENT_EMAILS)}")
    
    # Try to send test email
    print("\n📧 Sending test email...")
    
    try:
        subject = "SEAL Test Email - Email Setup Successful!"
        body = """
This is a test email from your SEAL contact form server.

If you're reading this, email notifications are working correctly!

Your contact form submissions will now be sent to:
- gregory.rhoney@fora.travel
- gregory.rhoney@gmail.com

Next steps:
1. Delete this test email
2. Start your servers with: .\\start_servers.ps1
3. Test the contact form at: http://localhost:8000/contact.html

---
SEAL Contact Form Server
"""
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(RECIPIENT_EMAILS)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print("✓ Test email sent successfully!")
        print(f"\n✅ Check your inbox at:")
        for email in RECIPIENT_EMAILS:
            print(f"   - {email}")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Failed to send test email!")
        print(f"   Error: {str(e)}")
        print("\nCommon fixes:")
        print("   1. Make sure you're using an app password (not your regular password)")
        print("   2. Enable 2-Step Verification in your Google Account")
        print("   3. Remove any spaces from the app password")
        print("   4. Generate a new app password\n")

if __name__ == '__main__':
    main()
