from typing import Optional

from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):

    kafka_broker_address: str
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_consumer_group: str
    ohlcv_window_seconds: int

    live_or_historical: Optional[str] = None
    last_n_days: Optional[int] = None

    class Config:
        env_file = ".env"

config = AppConfig()
