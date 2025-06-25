# Python Email Automation (Personalized Email Sender)

This project allows you to **automate sending personalized emails** to multiple recipients using **Python**. It includes:

- Personalized greetings like `Dear <Name>`
- Email body loaded from a `.txt` file
- Recipient list from a `.csv` file
- Support for multiple CC recipients
- Secure Gmail login using App Password

---

## Project Structure

```
email-automation/
├── contacts.csv         # Recipient list with optional CCs
├── email_body.txt       # Email body with {{name}} placeholder
├── send_emails.py       # Python script to send emails
├── requirements.txt     # Dependency list
└── README.md            # This file
```

---

## 🪠 Steps to Setup and Run

### 1. Download the Code

- Clone the repository or download the ZIP file from GitHub and extract it.

```bash
git clone https://github.com/your-username/email-automation.git
cd email-automation
```

---

### 2. Create and Activate a Virtual Environment

```bash
python -m venv env
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, use:

```bash
pip install secure-smtplib
```

---

### 4. Enable Gmail App Password

> You must enable **2-Step Verification** on your Gmail account first.

#### Steps:

1. Go to [https://myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Navigate to **App Passwords**
4. Select:

   - App: `Mail`
   - Device: `Other` (e.g., Python Script)

5. Click **Generate** and copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

---

### 5. Edit Script Variables

Open `send_emails.py` and update:

```python
sender_email = "your_email@gmail.com"
app_password = "your_generated_app_password"
subject = "Your Subject Here"
```

---

### 6. Create or Modify `email_body.txt`

Write your email content with `{{name}}` for personalization:

```
Dear {{name}},

This is a sample message sent using Python automation.
Best regards,
Your Name
```

---

### 7. Create or Modify `contacts.csv`

Example CSV format:

```
FirstName,LastName,EmailAddress,CcEmails
Sudeep,B,sudeep@gmail.com,"cc1@example.com,cc2@example.com"
Amithesh,Sharavanan,amithesh@gmail.com,""
```

---

### 8. Run the Script

```bash
python send_emails.py
```

Expected Output:

```
Sent to Sudeep <sudeep@gmail.com>
Sent to Amithesh <amithesh@gmail.com>
```

---

## Script Overview

The script:

- Reads `contacts.csv`
- Loads `email_body.txt`
- Replaces `{{name}}` with first name
- Sends emails via Gmail SMTP with CC support

---

## Important Notes

- Gmail's free tier has a daily email sending limit (\~500/day)
- Use App Password, not your main Gmail password
- Start testing with only your own email addresses
- Don't push `.env`, password, or secret files to GitHub
