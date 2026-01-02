import smtplib, ssl, yaml, os
from email.message import EmailMessage

with open("metadata/application.yaml") as f:
    data = yaml.safe_load(f)

sender = os.environ["EMAIL_USER"]
password = os.environ["EMAIL_PASS"]

msg = EmailMessage()
msg["From"] = sender
msg["To"] = data["to_email"]
msg["Subject"] = data["subject"]
msg.set_content(data["message"])

with open(data["resume_path"], "rb") as f:
    file_data = f.read()
    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename="Resume.pdf")

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender, password)
    server.send_message(msg)

print("Email sent successfully")
