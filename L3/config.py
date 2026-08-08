from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    ACCESS_TIME_IN_MINUTES: int
    SECRET_KEY: str

    ALGORITHM: str

    SUPERADMIN_PASSWORD: str

    B2_ENDPOINT_URL: str
    B2_ACCESS_KEY_ID: str
    B2_SECRET_ACCESS_KEY: str
    B2_BUCKET_NAME: str

    MAX_UPLOAD_SIZE_MB: int = 10
    USER_STORAGE_QUOTA_MB: int = 50
    ALLOWED_EXTENSIONS: str = "pdf,docx,doc,txt,png,jpg,jpeg"

    SMTP_HOST: str = "smtp.resend.com"
    SMTP_PORT: int = 465
    SMTP_USERNAME: str = "resend"
    SMTP_PASSWORD: str
    EMAILS_FROM_EMAIL: str
    EMAIL_ENABLED: bool = True

    GROQ_API_KEY: str

    FRONTEND_URL: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
