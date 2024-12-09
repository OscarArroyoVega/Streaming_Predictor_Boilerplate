from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='settings.env')
    kafka_broker_address: str
    kafka_input_topic: str
    kafka_consumer_group: str

    feature_group_name: str
    feature_group_version: int


config = Settings()


class HopsworksCredentials(BaseSettings):
    model_config = SettingsConfigDict(env_file='credentials.env')
    hopsworks_api_key: str


hopsworks_credentials = HopsworksCredentials()
