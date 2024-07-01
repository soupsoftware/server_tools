# Server Tools

A collection of useful scripts and tools for server management and automation. Currently it contains a module for sending emails with optional attachments via SMTP. It is designed to be secure, flexible, and easy to use, leveraging environment variables for sensitive information and providing command-line arguments for email configuration.

## Features

- **SMTP Connection**: Uses the `smtplib` library to handle SMTP connections and send emails.
- **Environment Variables**: Utilizes environment variables for sensitive information like SMTP server details and email account credentials.
- **MIME Emails**: Constructs MIME-compliant email messages, allowing for plain text bodies and file attachments.
- **Command-Line Arguments**: Provides flexibility for email configuration through command-line arguments.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/server_tools.git
    cd server_tools
    ```

2. Navigate to the email sending script directory:
    ```sh
    cd email_sending_script
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project directory and add your SMTP server details and email credentials:
    ```sh
    SMTP_SERVER=smtp-mail.outlook.com
    SMTP_PORT=587
    EMAIL_ACCOUNT=your_email@example.com
    EMAIL_PASSWORD=your_password
    ```

## Usage

Run the script with the required command-line arguments to send an email with or without attachments:

```sh
python send_email.py -e your_email@example.com -p your_password -r recipient@example.com -s "Test Subject" -b "This is a test email." -a /path/to/file1 /path/to/file2
```

