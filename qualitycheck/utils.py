from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP


def send_email_message(message, subject, email_from, email_to, smtp_server):
    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = email_to

    message_part = MIMEText(message, 'plain')

    msg.attach(message_part)

    with SMTP(smtp_server) as smtp:
        smtp.send_message(msg)
