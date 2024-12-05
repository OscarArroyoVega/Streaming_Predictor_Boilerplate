from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    kafka_broker_address: str
    kafka_topic: str
    pairs: List[str]

config = Config()