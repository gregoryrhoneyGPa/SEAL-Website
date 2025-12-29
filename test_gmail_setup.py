"""
Quick test script to verify Gmail integration is working
Run this after setting up credentials.json
"""
import os
import sys

def check_setup():
    print("\n" + "="*60)
    print("GMAIL INTEGRATION CHECK")
    print("="*60 + "\n")
    
    # Check for credentials
    if os.path.exists('credentials.json'):
        print("✅ credentials.json found")
    else:
        print("❌ credentials.json NOT found")
        print("   Follow GMAIL_SETUP.md to download this file\n")
        return False
    
    # Check for token (authentication status)
    if os.path.exists('token.json'):
        print("✅ token.json found (already authenticated)")
    else:
        print("⚠️  token.json not found (need to authenticate)")
        print("   This is normal for first-time setup")
        print("   Will authenticate when you start server.py\n")
    
    # Try to import required packages
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        print("✅ Google API packages installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("   Run: pip install google-auth-oauthlib google-api-python-client\n")
        return False
    
    print("\n" + "="*60)
    print("Setup Status: READY")
    print("="*60)
    print("\nNext steps:")
    print("1. Start server: & '.venv\\Scripts\\python.exe' server.py")
    print("2. If first time: Browser will open for authentication")
    print("3. Grant permissions in browser")
    print("4. Test form at: http://localhost:8000/contact.html")
    print("\n")
    return True

if __name__ == '__main__':
    success = check_setup()
    sys.exit(0 if success else 1)
