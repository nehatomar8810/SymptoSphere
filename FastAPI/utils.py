from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def send_email(email: str):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = settings.email
    password = settings.smtp_password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = 'SymptoSphere Website'
    
    disclaimer = "This is a system-generated email. Please do not respond."
    body = (
    f'Welcome to SymptoSphere!\nYou are receiving this email because you recently created a new SymptoSphere account or '
    f'added a new email address. If this was not you, please ignore this email.\n\n\n\n\n\n\n\n\nThis email was sent to {email}, '
    f'which is associated with a SymptoSphere account.\n\n{disclaimer}')

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)