from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "QuUD API"
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
