# mock for kraken api
from pydantic import BaseModel
from typing import List
from datetime import datetime

class Trade(BaseModel):
    pair: str
    price: float
    volume: float
    timestamp: datetime
    timestamp_ms: int
    
    def to_dict(self) -> dict:
        return self.model_dump()
    
class KrakenApi:

    def __init__(self,pair: str):
        self.pair = pair

    def get_trades(self, pair: str) -> List[Trade]:
        mock_trades = [
            Trade(pair=self.pair, price=0.5027, volume=144.12, timestamp=datetime(2024, 2, 12, 14, 43, 23, 123456), timestamp_ms=1),
            Trade(pair=self.pair, price=0.5018, volume=23.12 , timestamp=datetime(2024, 2, 12, 14, 43, 24, 123456), timestamp_ms=2),
            Trade(pair=self.pair, price=0.5039, volume=32.0013 , timestamp=datetime(2024, 2, 12, 14, 43, 25, 123456), timestamp_ms=3),
            Trade(pair=self.pair, price=0.5030, volume=33.46326, timestamp=datetime(2024, 2, 12, 14, 43, 26, 123456), timestamp_ms=4),
        ]
        return mock_trades
