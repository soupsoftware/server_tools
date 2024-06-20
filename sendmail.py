import smtplib
import socket
import argparse
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv


load_dotenv()

# Email account credentials
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp-mail.outlook.com')
SMTP_PORT = os.getenv('SMTP_PORT', '587')
HOSTNAME = socket.gethostname()

def send_email(email_account, password, recipient, subject, body, attachments):
    """
    Sends an email using SMTP with optional attachments.

    Args:
        email_account (str): The email account to send from.
        password (str): The password or app-specific password for the email account.
        recipient (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body of the email.
        attachments (list): List of file paths to attach to the email.

    Returns:
        None
    """
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = email_account
    msg['To'] = recipient
    msg['Subject'] = f"Alert@{HOSTNAME}: " + subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    for file_path in attachments:
        try:
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(file_path)}')
                msg.attach(part)
        except Exception as e:
            print(f"Failed to attach file {file_path}: {e}")

    # Send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()  # Identify ourselves to the SMTP server
        server.starttls()  # Secure the SMTP connection
        server.ehlo()  # Re-identify ourselves over the secure connection
        server.login(email_account, password)
        server.sendmail(email_account, recipient, msg.as_string())
        print("Email sent successfully.")
        server.quit()
    except smtplib.SMTPAuthenticationError:
        print("Failed to send email: Authentication error. Check your username and password.")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """
    Main function to parse command-line arguments and send an email.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Send an email with optional attachments via SMTP.')
    parser.add_argument('-e', '--email_account', type=str, default=os.getenv('EMAIL_ACCOUNT'), help='The email account to send from.')
    parser.add_argument('-p', '--password', type=str, default=os.getenv('EMAIL_PASSWORD'), help='The password or app-specific password for the email account.')
    parser.add_argument('-r', '--recipient', type=str, default=os.getenv('EMAIL_ACCOUNT'), help='The recipient\'s email address.')
    parser.add_argument('-s', '--subject', type=str, default='Test', help='The subject of the email.')
    parser.add_argument('-b', '--body', type=str, default='This is a test email.', help='The body of the email.')
    parser.add_argument('-a', '--attachments', nargs='*', default=[], help='List of file paths to attach to the email.')

    args = parser.parse_args()

    send_email(args.email_account, args.password, args.recipient, args.subject, args.body, args.attachments)

if __name__ == '__main__':
    main()

