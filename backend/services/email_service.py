import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.utils.logging_utils import *


class EmailService:

    def __init__(self):
        self.sender_name = "IntelliTrader"
        self.sender_email = "developer.intellitrader@gmail.com"
        self.email_password = "aene ifwj rdxf nwgu"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    # Send Email
    def send_email(self, recipient_email, template, **kwargs):
        """
        Sends an email with the provided details.

        Args:
            recipient_email (str): The email address of the recipient.
            template (str): The template name to use for the email.
            **kwargs: Additional keyword arguments to format the email body.

        Returns:
            dict: A dictionary with the success status and error message if any.
        """
        if not recipient_email or not template:
            raise ValueError(
                "Recipient email and template are required to send an email."
            )

        subject = self.get_mail_subject(template)
        body = self.get_mail_body(template, **kwargs)

        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = (
            subject + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        message.attach(MIMEText(body, "html" if "<html>" in body else "plain"))

        try:
            mailserver = smtplib.SMTP(self.smtp_server, self.smtp_port)
            mailserver.ehlo()
            mailserver.starttls()
            mailserver.ehlo()
            mailserver.login(self.sender_email, self.email_password)
            mailserver.sendmail(self.sender_email, recipient_email, message.as_string())
            mailserver.quit()
            return {"success": True, "data": None}

        except Exception as error:
            return {"success": False, "error": str(error)}

    # Get Mail Subject
    def get_mail_subject(self, template):
        """
        Retrieves the subject for the email based on the template.

        Args:
            template (str): The template name.

        Returns:
            str: The subject of the email.
        """
        subjects = {"forgot_password": "Password Reset Link "}
        return subjects[template]

    # Get Mail Body
    def get_mail_body(self, template, **kwargs):
        """
        Retrieves the body for the email based on the template.

        Args:
            template (str): The template name.
            **kwargs: Additional keyword arguments to format the email body.

        Returns:
            str: The body of the email.

        Raises:
            ValueError: If the template name is invalid.
        """
        templates = {
            "forgot_password": """
                <html>
                <body>
                    <p>You have requested a password reset for your account.</p>
                    <p>Please click the following link to reset your password:</p>
                    <a href="{reset_link}">Reset Password</a>
                </body>
                </html>
            """,
            # Add more templates here as needed
        }

        if template in templates:
            return templates[template].format(**kwargs)
        else:
            raise ValueError(f"Invalid template name: {template}")
