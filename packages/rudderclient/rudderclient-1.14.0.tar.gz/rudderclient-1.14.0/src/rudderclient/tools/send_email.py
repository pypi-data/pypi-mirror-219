import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders


def read_template(file, replacements):
    """
    Read an HTML file and replace placeholders with actual values.

    :param file: Path to the HTML file.
    :param replacements: A dictionary where the keys are the placeholder names and the values are the replacement strings.
    :return: The content of the HTML file with placeholders replaced.
    """
    try:
        with open(file, "r") as f:
            content = f.read()
        for key, value in replacements.items():
            content = content.replace("{{ " + key + " }}", value)
        return content
    except FileNotFoundError:
        print(f"Error: File {file} not found.")
        return None


def attach_files(msg, attachment_dir):
    """
    Attach files to the email message.

    :param msg: The email message object.
    :param attachment_dir: Path to the directory containing the files to attach.
    """
    for file_name in os.listdir(attachment_dir):
        file_path = os.path.join(attachment_dir, file_name)
        try:
            with open(file_path, "rb") as f:
                if file_name.endswith("logo.png"):
                    img = MIMEImage(f.read())
                    img.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename="logo.png",
                    )
                    img.add_header("Content-ID", "<logo.png>")
                    msg.attach(img)
                else:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition", "attachment", filename=file_name
                    )
                    msg.attach(part)
        except FileNotFoundError:
            print(f"Error: Attachment file {file_path} not found.")


def send_email(
    smtp_username,
    smtp_password,
    from_address,
    to_address,
    subject,
    cc_address=None,
    html_file=None,
    attachment_dir=None,
    replacements=None,
):
    """
    Send an email using AWS SMTP.

    :param smtp_username: The AWS SMTP username.
    :param smtp_password: The AWS SMTP password.
    :param from_address: The sender's email address.
    :param to_address: The recipient's email address.
    :param subject: The email subject.
    :param cc_address: (Optional) The CC email address.
    :param html_file: (Optional) Path to the HTML file to use as the email body.
    :param attachment_dir: (Optional) Path to the directory containing the files to attach.
    :param replacements: (Optional) A dictionary where the keys are the placeholder names in the HTML file and the values are the replacement strings.
    """
    try:
        with smtplib.SMTP("email-smtp.us-east-1.amazonaws.com", 587) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)

            msg = MIMEMultipart()
            msg["From"] = from_address
            msg["To"] = to_address
            msg["Subject"] = subject
            if cc_address:
                msg["Cc"] = cc_address

            if html_file and replacements:
                html = read_template(html_file, replacements)
                if html:
                    msg.attach(MIMEText(html, "html"))

            if attachment_dir:
                attach_files(msg, attachment_dir)

            text = msg.as_string()
            server.sendmail(from_address, to_address, text)
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
