import json
import re
import time
from playwright.sync_api import sync_playwright

URL = "https://www.ctis.bilkent.edu.tr/ctis_internship_firms.php"

def extract_email(text):
    # Regex to find email addresses
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print(f"Navigating to {URL}...")
        page.goto(URL)

        # 1. Force wait for the table to appear
        try:
            print("Waiting for table to load...")
            page.wait_for_selector('table tbody tr', timeout=5000)
        except:
            print("❌ Error: Could not find any table on the page.")
            browser.close()
            return

        # 2. Try to expand to 100 entries (Generic selector)
        try:
            page.select_option('select[name*="length"]', "100")
            time.sleep(2)
        except:
            print("Could not expand table, sticking to default 10.")

        all_companies = []
        
        while True:
            # 3. GENERIC SELECTOR: Grab rows from ANY table with a body
            # This ignores the specific ID "DataTables_Table_0" which might be wrong
            rows = page.locator('table tbody tr').all()
            
            count = len(rows)
            print(f"Scraping {count} rows on this page...")

            for row in rows:
                # Get all cells (columns) in this row
                columns = row.locator('td').all()
                
                # If row has fewer than 2 columns, it's probably empty or a header
                if len(columns) < 2: 
                    continue

                # CTIS structure usually: Name=0, City=1, ... Contact=4
                name = columns[0].inner_text().strip()
                city = columns[1].inner_text().strip()
                
                # Extract text from all columns to be safe
                full_text = row.inner_text()
                email = extract_email(full_text)

                if email:
                    print(f"✅ Found: {name} ({email})")
                    all_companies.append({
                        "name": name, 
                        "email": email, 
                        "city": city, 
                        "status": "Not Applied"
                    })
                else:
                    # Save it anyway for manual checking
                    # print(f"⚠️ No email for {name}") 
                    all_companies.append({
                        "name": name, 
                        "email": "Missing", 
                        "city": city, 
                        "status": "Manual Check Needed"
                    })

            # 4. Handle "Next" Button
            # Look for a button with text "Next" or class "next"
            next_btn = page.locator('.paginate_button.next')
            
            # Check if it's disabled (end of list)
            classes = next_btn.get_attribute("class")
            if not classes or "disabled" in classes:
                print("Reached the last page.")
                break
            
            next_btn.click()
            time.sleep(1) # Wait for new rows to load

        # Save
        with open('ctis_companies.json', 'w', encoding='utf-8') as f:
            json.dump(all_companies, f, indent=4, ensure_ascii=False)
        
        print(f"🎉 Done! Scraped {len(all_companies)} companies.")
        browser.close()

if __name__ == "__main__":
    run()