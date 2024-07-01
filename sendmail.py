"""
This module provides functionality to send emails with optional attachments via SMTP.

Design:
- The module leverages the smtplib library to handle SMTP connections and send emails.
- Environment variables are used to store sensitive information such as SMTP server details and email account credentials.
- The dotenv library is used to load environment variables from a .env file, ensuring that credentials are not hard-coded in the script.
- The email.mime libraries are utilized to construct MIME-compliant email messages, allowing for plain text bodies and file attachments.

Control Flow:
1. Environment Setup:
   - Environment variables are loaded from a .env file using load_dotenv.
   - SMTP server details and hostname are fetched from environment variables.

2. Main Function:
   - The main() function parses command-line arguments using argparse.
   - Parsed arguments include email account details, recipient address, email subject, body, and optional attachments.

3. Sending Email:
   - The send_email function constructs an email message with the provided details.
   - File attachments are read, encoded in base64, and attached to the email.
   - An SMTP connection is established using the provided SMTP server and port.
   - The email account credentials are used to log in to the SMTP server.
   - The email is sent, and appropriate error handling is implemented for potential issues such as authentication errors or SMTP exceptions.

Usage:
- This script can be run from the command line with appropriate arguments to send an email with or without attachments.
- It is designed to be flexible and secure, leveraging environment variables for sensitive information and providing clear error messages in case of failures.

Example:
    python send_email.py -e your_email@example.com -p your_password -r recipient@example.com -s "Test Subject" -b "This is a test email." -a /path/to/file1 /path/to/file2
"""

import argparse
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import socket

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Email account credentials and server configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp-mail.outlook.com')  # Default to Outlook's SMTP server if not set
SMTP_PORT = os.getenv('SMTP_PORT', '587')  # Default to port 587 for TLS
HOSTNAME = socket.gethostname()  # Get the hostname of the machine to include in the email subject

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
    # Create the email message container
    msg = MIMEMultipart()
    msg['From'] = email_account
    msg['To'] = recipient
    msg['Subject'] = f"Alert@{HOSTNAME}: " + subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach files to the email
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

    # Send the email via SMTP
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()  # Identify ourselves to the SMTP server
            server.starttls()  # Secure the SMTP connection
            server.ehlo()  # Re-identify ourselves over the secure connection
            server.login(email_account, password)
            server.sendmail(email_account, recipient, msg.as_string())
            print("Email sent successfully.")
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

    # Call the send_email function with the parsed arguments
    send_email(args.email_account, args.password, args.recipient, args.subject, args.body, args.attachments)

if __name__ == '__main__':
    main()
