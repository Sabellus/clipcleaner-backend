from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_token: str
    yookassa_shop_id: str
    yookassa_secret_key: str

    class Config:
        env_file = ".env"  # для локального запуска без Docker

settings = Settings()
