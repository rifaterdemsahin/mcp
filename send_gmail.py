import smtplib
import ssl
from email.message import EmailMessage
import getpass

# Read recipient email from emails.md
with open('emails.md', 'r') as f:
    lines = f.readlines()
    recipient = None
    for line in lines:
        if '@' in line:
            recipient = line.strip().split()[-1]
            break
    if not recipient:
        raise ValueError('No recipient email found in emails.md')

# Read subject and body from email_content.md
with open('email_content.md', 'r') as f:
    lines = f.readlines()
    subject = ''
    body_lines = []
    for line in lines:
        if line.lower().startswith('subject:'):
            subject = line[len('Subject:'):].strip()
        else:
            body_lines.append(line)
    body = ''.join(body_lines).strip()

# Email details
sender = 'info@pexabo.com'

# Prompt for app password securely
app_password = getpass.getpass('Enter Gmail app password for info@pexabo.com: ')

# Create the email
msg = EmailMessage()
msg['From'] = sender
msg['To'] = recipient
msg['Subject'] = subject
msg.set_content(body)

# Send the email via Gmail SMTP
context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
    server.login(sender, app_password)
    server.send_message(msg)

print(f'Email sent to {recipient} from {sender}') 