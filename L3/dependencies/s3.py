import uuid
import io
import boto3
from fastapi import UploadFile, HTTPException
from config import settings

from urllib.parse import urlparse

B2_REGION = urlparse(settings.B2_ENDPOINT_URL).hostname.split(".")[1]

s3 = boto3.client(
    "s3",
    endpoint_url=settings.B2_ENDPOINT_URL,
    aws_access_key_id=settings.B2_ACCESS_KEY_ID,
    aws_secret_access_key=settings.B2_SECRET_ACCESS_KEY,
    region_name=B2_REGION,
)

ALLOWED_EXTENSIONS = {ext.strip().lower() for ext in settings.ALLOWED_EXTENSIONS.split(",") if ext.strip()}
MAX_UPLOAD_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


class UploadService:
    @staticmethod
    async def upload_file(file: UploadFile):
        ext = (file.filename.split(".")[-1] or "").lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type '.{ext}' not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}",
            )

        size = 0
        chunks = []
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_UPLOAD_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail=f"File exceeds max size of {settings.MAX_UPLOAD_SIZE_MB} MB",
                )
            chunks.append(chunk)

        if size == 0:
            raise HTTPException(status_code=400, detail="Empty file")

        key = f"uploads/{uuid.uuid4()}.{ext}"
        try:
            s3.put_object(
                Bucket=settings.B2_BUCKET_NAME,
                Key=key,
                Body=io.BytesIO(b"".join(chunks)),
                ContentType=file.content_type or "application/octet-stream",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"B2 upload failed: {str(e)}")

        return key, size

    @staticmethod
    def delete_file(key: str):
        if not key:
            return
        try:
            s3.delete_object(Bucket=settings.B2_BUCKET_NAME, Key=key)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"B2 delete failed: {str(e)}")

    @staticmethod
    def get_object(key: str):
        try:
            return s3.get_object(Bucket=settings.B2_BUCKET_NAME, Key=key)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")
