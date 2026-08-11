from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bucket_name: str
    document_table: str
    user_table: str
    chat_table: str
    conversation_table: str
    connections_table: str

    jwt_private_key: str
    jwt_public_key: str

    textract_topic_arn: str
    textract_role_arn: str

    neon_database_url: str
    websocket_endpoint: str
    redis_host: str
    redis_port: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
