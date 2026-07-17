import uuid
import boto3
from fastapi import UploadFile, HTTPException
from config import settings

s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)

class UploadService:
    @staticmethod
    async def upload_file(file: UploadFile):
        ext = file.filename.split(".")[-1]
        key = f"uploads/{uuid.uuid4()}.{ext}"
        try:
            s3.upload_fileobj(
                file.file,
                settings.AWS_BUCKET_NAME,
                key,
                ExtraArgs={"ContentType": file.content_type},
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")

        return f"https://{settings.AWS_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
