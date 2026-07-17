import boto3
from botocore.exceptions import ClientError
from config import settings
ses_client = boto3.client(
    "ses",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name="ap-south-1"
)

class EmailService:

    @staticmethod
    def send_email(to_email: str, subject: str, html_body: str):
        try:
            ses_client.send_email(
                Source=settings.EMAILS_FROM_EMAIL,
                Destination={"ToAddresses": [to_email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Html": {"Data": html_body}},
                },
            )
        except ClientError as e:
            raise Exception(f"SES email failed: {e.response['Error']['Message']}")

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
