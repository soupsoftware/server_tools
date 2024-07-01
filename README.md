# Server Tools

A collection of useful scripts and tools for server management and automation. Currently the sole module focuses on sending emails with optional attachments via SMTP. It is designed to be secure, flexible, and easy to use, leveraging environment variables for sensitive information and providing command-line arguments for email configuration.

## Features

- **SMTP Connection**: Uses the `smtplib` library to handle SMTP connections and send emails.
- **Environment Variables**: Utilizes environment variables for sensitive information like SMTP server details and email account credentials.
- **MIME Emails**: Constructs MIME-compliant email messages, allowing for plain text bodies and file attachments.
- **Command-Line Arguments**: Provides flexibility for email configuration through command-line arguments.

## Requirements

- **Python**: Ensure you have Python 3.6 or higher installed. [Download Python](https://www.python.org/)
- **pip**: Python package installer, usually comes with Python. [Install pip](https://pip.pypa.io/en/stable/installation/)
- **pipenv**: Python dependency management tool. Install via:
    ```sh
    pip install pipenv
    ```
- **smtplib**: Built-in Python library for sending emails via SMTP.
- **socket**: Built-in Python library for networking and hostname resolution.
- **argparse**: Built-in Python library for parsing command-line arguments.
- **os**: Built-in Python library for interacting with the operating system.
- **email.mime**: Built-in Python libraries for constructing MIME-compliant emails.
- **dotenv**: External library for loading environment variables from a `.env` file. Install via:
    ```sh
    pipenv install python-dotenv
    ```

### Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/soupsoftware/server_tools.git
    cd server_tools
    ```
    
2. Install dependencies:
    ```sh
    pipenv install
    ```

3. Activate the virtual environment:
    ```sh
    pipenv shell
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
