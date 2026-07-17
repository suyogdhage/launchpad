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
    def send_email(to_email: str,subject: str,html_body: str):
       
        try:
            response = ses_client.send_email(Source=settings.EMAILS_FROM_EMAIL,Destination={"ToAddresses": [to_email]},
    Message={"Subject": {"Data": subject},"Body": {"Html": {"Data": html_body}}})

        except ClientError as e:
            raise Exception(
                f"SES email failed: {e.response['Error']['Message']}")

    @staticmethod
    def send_login(to_email: str,subject: str,message: str,) :

        html = f"""
        <p>{message}</p>
        <p>
            <a>
                Sign-In
            </a>
        </p>
        """
        EmailService.send_email(to_email=to_email,subject=subject,html_body=html)


email_service = EmailService()
