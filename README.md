# 📧 Internship Application Automator

A Python-based automation toolkit designed to streamline the process of applying for internships. This project includes scripts to scrape company contact information and automate sending personalized application emails with attachments (CVs).
I highly recommend to check the scape part as I made it for my own website so it wont work for u, just Scrape the company name and the its mail that u will apply the rest it automated mail

## 🚀 Features

* **Automated Emailing (`applier_stable.py`):** Sends personalized emails to a list of companies using SMTP.
* **Attachment Handling:** Automatically attaches your PDF CV to every email.
* **Company Scraper (`scraper.py`):** Collects company names and email addresses from target websites/lists and saves them to a JSON database.
* **Data Management:** Uses `ctis_companies.json` to store and manage the status of applications.

## 📂 Project Structure

* `applier_stable.py` - The main script that reads the company list and sends the applications.
* `scraper.py` - Utility script to gather company data.
* `ctis_companies.json` - The database containing company names and emails.
* `CV.pdf` - (Local only) The resume file sent as an attachment.

## 🛠️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ayalgasimli/internship-automation.git](https://github.com/ayalgasimli/internship-automation.git)
    cd internship-automation
    ```

2.  **Add your CV:**
    Place your resume in the root folder and rename it to `CV.pdf` (or update the script to match your filename).

3.  **Configure Credentials:**
    * Open `applier_stable.py`.
    * Locate the email configuration section.
    * **Note:** For Gmail, you must use an **App Password**, not your regular login password. (Go to Google Account > Security > 2-Step Verification > App Passwords).

## 💻 Usage

### 1. Gather Company Data
If you don't have a list yet, run the scraper:
```bash
python scraper.py
