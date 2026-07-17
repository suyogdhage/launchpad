from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    ACCESS_TIME_IN_MINUTES: int
    SECRET_KEY:str

    ALGORITHM: str

    SUPERADMIN_PASSWORD: str

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_BUCKET_NAME: str
    EMAILS_FROM_EMAIL:str
    GROQ_API_KEY:str
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")


settings = Settings()






    
