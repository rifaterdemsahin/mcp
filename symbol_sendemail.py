import smtplib
from email.message import EmailMessage

# ⚠️ Replace these with your actual email and password (or App Password if using Gmail with 2FA)
EMAIL_ADDRESS = 'XXX@example.com'
EMAIL_PASSWORD = 'XXX'  # Replace with your real email password or app-specific password

# 🎯 Set up email details
msg = EmailMessage()
msg['Subject'] = '🎉 Hello from Python!'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'recipient@example.com'  # Replace with the recipient's email address
msg.set_content('Hi there!\n\nThis email was sent from a Python script using smtplib.\n\nCheers! 🐍')

# 🚀 Send the email via SMTP server
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("✅ Email sent successfully.")
except Exception as e:
    print("❌ Failed to send email:", e)
