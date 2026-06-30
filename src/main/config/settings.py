from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bucket_name: str
    document_table: str
    user_table: str

    jwt_private_key: str
    jwt_public_key: str

    textract_topic_arn: str
    textract_role_arn: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
