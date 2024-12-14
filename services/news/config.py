from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Config class for the news service
    """

    model_config = SettingsConfigDict(env_file='settings.env')
    kafka_broker_address: str
    kafka_topic: str
    polling_interval_sec: int


config = Config()


class CryptopanicConfig(BaseSettings):
    """
    Config class for the cryptopanic api
    """

    model_config = SettingsConfigDict(env_file='cryptopanic_credentials.env')
    cryptopanic_api_key: str


cryptopanic_config = CryptopanicConfig()
