import smtplib
import ssl
from email.message import EmailMessage
from config import settings
from dependencies.loggers import logger


class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, html_body: str):
        if not settings.EMAIL_ENABLED:
            logger.info(f"Email disabled, skipping to {to_email}: {subject}")
            return

        msg = EmailMessage()
        msg["From"] = settings.EMAILS_FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(html_body)
        msg.add_alternative(html_body, subtype="html")

        try:
            if settings.SMTP_PORT == 465:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context) as server:
                    server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                    server.starttls()
                    server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                    server.send_message(msg)
            logger.info(f"Email sent to {to_email}: {subject}")
        except Exception as e:
            raise Exception(f"SMTP email failed: {e}")

    @staticmethod
    def send_document_approved(to_email: str):
        html = """
        <h2>Document Approved</h2>

        <p>Your uploaded document has been <b>approved</b>.</p>

        <p>You may now continue with the next stage of the workflow.</p>

        <br>
        <p>Regards,</p>
        <p>Document Management Team</p>
        """

        EmailService.send_email(
            to_email=to_email,
            subject="Document Approved",
            html_body=html,
        )

    @staticmethod
    def send_document_rejected(to_email: str, reason: str):
        html = f"""
        <h2>Document Rejected</h2>

        <p>Your uploaded document has been <b>rejected</b>.</p>

        <p><b>Reason:</b> {reason}</p>

        <p>Please correct the document and upload it again.</p>

        <br>
        <p>Regards,</p>
        <p>Document Management Team</p>
        """

        EmailService.send_email(
            to_email=to_email,
            subject="Document Rejected",
            html_body=html,
        )


email_service = EmailService()
