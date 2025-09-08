import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail login details
sender_email = "0863ad231028@gmail.com"
password = "eejq uenu stbt eafp"   # Gmail App Password
receiver_email = "aagamjain2704@gmail.com"

def SendEmail(subject="⚠ Alert: Person Count Notification", body="Person count has reached 10!"):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅ Email sent successfully to", receiver_email)
    except Exception as e:
        print("❌ Error:", e)