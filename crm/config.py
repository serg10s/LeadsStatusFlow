from pydantic_settings import BaseSettings, SettingsConfigDict

EMAIL_USE_SSL=True
API_KEY="ba67df6a-a17c-476f-8e95-bcdb75ed3958"  # test key
VERIFICATION_TOKEN_EXPIRE_HOURS=24
ALGORITHM="HS256"


class Settings(BaseSettings):
    EMAIL_HOST: str 
    EMAIL_PORT: str
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str
    SECRET_KEY: str
    BASE_URL: str
    TG_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
