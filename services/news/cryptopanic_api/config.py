from pydantic_settings import BaseSettings, SettingsConfigDict


class CryptopanicConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='cryptopanic.credentials.env')
    cryptopanic_api_key: str


config = CryptopanicConfig()
