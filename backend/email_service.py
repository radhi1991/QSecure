import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
SMTP_SERVER = 'smtp.example.com'  # Replace with your SMTP server
SMTP_PORT = 587  # Replace with your SMTP port
SMTP_USERNAME = 'your_email@example.com'  # Replace with your email
SMTP_PASSWORD = 'your_password'  # Replace with your email password


def send_email_confirmation(recipient_email, file_name):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = recipient_email
    msg['Subject'] = 'File Shared Successfully'

    # HTML email template
    html = f"""
    <html>
    <body>
        <h1>Your file has been shared!</h1>
        <p>The file <strong>{file_name}</strong> has been successfully shared with you.</p>
        <p>Please visit your dashboard to download the file.</p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
