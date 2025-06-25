import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "spacesudeep07@gmail.com"  # Your email
app_password = "whjt gwxi tmxv pwzf"  # Your App Password
subject = "Personalized Email via Python"
csv_file = "contacts.csv"
body_file = "email_body.txt"

with open(body_file, "r", encoding="utf-8") as f:
    body_template = f.read()


def send_email(to_email, cc_emails, first_name):
    body_customized = body_template.replace("{{name}}", first_name)

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Cc"] = ", ".join(cc_emails) if cc_emails else ""
    msg["Subject"] = subject
    msg.attach(MIMEText(body_customized, "plain"))

    all_recipients = [to_email] + cc_emails

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, all_recipients, msg.as_string())
        print(f"Sent to {first_name} <{to_email}> with CC to {cc_emails}")
    except Exception as e:
        print(f"Failed to send to {to_email}: {e}")


with open(csv_file, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        first_name = row["FirstName"].strip()
        to_email = row["EmailAddress"].strip()
        cc_raw = row.get("CcEmails", "").strip()
        cc_emails = [email.strip() for email in cc_raw.split(",") if email]
        send_email(to_email, cc_emails, first_name)
