import smtplib
import ssl
import threading
from email.message import EmailMessage
from config import settings
from dependencies.loggers import logger

SMTP_TIMEOUT_SECONDS = 15


class EmailService:
    @staticmethod
    def _smtp_send(to_email: str, subject: str, html_body: str):
        if not settings.EMAIL_ENABLED:
            logger.info(f"Email disabled, skipping to {to_email}: {subject}")
            return

        msg = EmailMessage()
        msg["From"] = settings.EMAILS_FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content("Please view this email in an HTML-capable client.")
        msg.add_alternative(html_body, subtype="html")

        try:
            if settings.SMTP_PORT == 465:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(
                    settings.SMTP_HOST, settings.SMTP_PORT, timeout=SMTP_TIMEOUT_SECONDS, context=context
                ) as server:
                    server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=SMTP_TIMEOUT_SECONDS) as server:
                    server.ehlo()
                    server.starttls(context=ssl.create_default_context())
                    server.ehlo()
                    server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                    server.send_message(msg)
            logger.info(f"Email sent to {to_email}: {subject}")
        except Exception as e:
            logger.warning(f"SMTP email failed to {to_email} ({subject}): {e}")

    @staticmethod
    def send_email(to_email: str, subject: str, html_body: str):
        threading.Thread(
            target=EmailService._smtp_send,
            args=(to_email, subject, html_body),
            daemon=True,
        ).start()

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
