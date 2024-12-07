from datetime import datetime

from pydantic import BaseModel, computed_field


class Trade(BaseModel):
    pair: str
    price: float
    volume: float
    timestamp: datetime

    @computed_field
    def timestamp_ms(self) -> int:
        return int(self.timestamp.timestamp() * 1000)

    def to_dict(self) -> dict:
        return self.model_dump(exclude={'timestamp'})
