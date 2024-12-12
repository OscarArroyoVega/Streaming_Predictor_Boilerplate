from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='settings.env')
    kafka_broker_address: str
    kafka_input_topic: str
    kafka_consumer_group: str

    feature_group_name: str
    feature_group_version: int
    feature_group_primary_keys: list[str]
    feature_group_event_time: str
    data_source: Literal['live', 'historical']


config = Settings()


class HopsworksCredentials(BaseSettings):
    model_config = SettingsConfigDict(env_file='hopsworks_credentials.env')
    hopsworks_api_key: str
    hopsworks_project_name: str


hopsworks_credentials = HopsworksCredentials()
