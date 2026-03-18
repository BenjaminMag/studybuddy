from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "StudySphere"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 60 * 8  # 8 hours
    university_email_domain: str = "benjamin.magloire@students.fhnw.ch"  # change to your domain
    max_file_size_bytes: int = 20 * 1024 * 1024  # 20MB

settings = Settings()