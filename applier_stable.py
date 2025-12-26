import json
import os
import time
import win32com.client as win32

# --- CONFIGURATION ---
CV_FILENAME = "CV.pdf"
MY_NAME = "Ayal Gasimli"
MY_MAJOR = "Computer Technology and Information Systems (CTIS)"
MY_PORTFOLIO = "https://linkedin.com/in/ayal" 

def get_outlook_app():
    """Connects to the open Outlook app and verifies it is ready."""
    try:
        # 1. Try to grab the running Outlook instance
        outlook = win32.GetActiveObject("Outlook.Application")
        
        # 2. "The Handshake": Try to read the user's name to prove we are connected
        namespace = outlook.GetNamespace("MAPI")
        user = namespace.CurrentUser.Name
        print(f"✅ Connected to Outlook as: {user}")
        return outlook
    except Exception as e:
        print("❌ Could not connect to Outlook.")
        print("👉 Make sure Outlook is OPEN and you are logged in.")
        return None

def create_draft(outlook, company, cv_path):
    try:
        # Reuse the SAME connection (outlook object)
        mail = outlook.CreateItem(0) 

        mail.To = company['email']
        mail.Subject = f"Internship Application - {MY_NAME} - Bilkent University"
        
        mail.HTMLBody = f"""
        <p>Dear Hiring Team at <b>{company['name']}</b>,</p>
        <p>I hope you are having a great week.</p>
        <p>My name is {MY_NAME}, a 3rd-year student at Bilkent University studying {MY_MAJOR}.</p>
        <p>I found your contact information through our university's partner list. I am writing to inquire about Summer/Semester internship opportunities at {company['name']}.</p>
        <p>I have a strong background in R, Python, and Data Science. I am eager to contribute to your team.<br>
        You can view my portfolio here: <a href="{MY_PORTFOLIO}">{MY_PORTFOLIO}</a></p>
        <p>My CV is attached to this email. Thank you for your time and consideration.</p>
        <p>Best regards,<br>{MY_NAME}</p>
        """

        mail.Attachments.Add(cv_path)
        mail.Display()
        return True

    except Exception as e:
        print(f"   ⚠️ Outlook Error: {e}")
        return False

def run():
    cv_path = os.path.abspath(CV_FILENAME)
    if not os.path.exists(cv_path):
        print(f"❌ ERROR: Could not find {CV_FILENAME}.")
        return

    # 1. CONNECT ONCE AT THE START
    print("Connecting to Outlook...")
    outlook = get_outlook_app()
    
    if not outlook:
        return # Stop if we can't connect

    # 2. Load Data
    with open('ctis_companies.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("------------------------------------------------")
    print(f"Loaded {len(data)} companies.")
    print("------------------------------------------------")
    input("👉 Press ENTER to start applying...")

    for company in data:
        if company.get('status') == "Applied": continue
        if company['email'] == "Missing": continue

        print(f"Drafting: {company['name']}...", end=" ")
        
        # Pass the EXISTING outlook object
        success = create_draft(outlook, company, cv_path)
        
        if success:
            print("✅ Open.")
            
            # Save progress
            company['status'] = "Applied"
            with open('ctis_companies.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            user = input("   👉 [Enter] Next | [exit] Stop: ")
            if user.lower() == 'exit': break
            
            # Tiny pause to let Outlook GUI catch up
            time.sleep(0.5)
        else:
            print("❌ Failed. (Waiting 5s and retrying...)")
            time.sleep(5)
            # Try one more time
            create_draft(outlook, company, cv_path)

if __name__ == "__main__":
    run()