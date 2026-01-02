import smtplib, ssl, os, yaml
from email.message import EmailMessage


with open("metadata/application.yaml") as f:
    app = yaml.safe_load(f)

with open("metadata/recipients.txt") as f:
    recipients = [line.strip() for line in f if line.strip()]

sender = os.environ["EMAIL_USER"]
password = os.environ["EMAIL_PASS"]

for email in recipients:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = email
    msg["Subject"] = app["subject"]
    msg.set_content(app["message"])

    with open(app["resume_path"], "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename="Resume.pdf")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password)
        server.send_message(msg)
