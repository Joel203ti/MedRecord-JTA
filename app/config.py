from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    azure_foundry_endpoint: str = ""
    azure_foundry_api_key: str = ""
    azure_foundry_model: str = "gpt-4o"
    max_upload_mb: int = 10
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings=Settings()
