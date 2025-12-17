import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings

def send_email(receiver,subject,body):
    sender = settings.EMAIL_NAME
    password = settings.EMAIL_PASSWORD
    

    

    # Build email message
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    # Connect to Gmail SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())

    print("Email sent successfully!")

