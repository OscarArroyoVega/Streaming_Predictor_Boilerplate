from datetime import datetime

from pydantic import BaseModel, computed_field


class Trade(BaseModel):
    pair: str
    price: float
    volume: float
    timestamp: datetime  # readable human

    @computed_field
    def timestamp_ms(
        self,
    ) -> int:  # add a computed field to get the timestamp in milliseconds as integer
        return int(self.timestamp.timestamp() * 1000)

    def to_dict(self) -> dict:
        return self.model_dump(exclude={'timestamp'})

    @classmethod
    def from_kraken_rest_api_response(
        cls, pair: str, price: float, volume: float, timestamp_sec: str
    ) -> 'Trade':
        """
        Returns a Trade object from the Kraken REST API response.

        E.g response:
            ['76395.00000', '0.01305597', 1731155565.4159515, 's', 'm', '', 75468573]

            price: float
            volume: float
            timestamp_sec: float
        """

        timestamp_ms = int(float(timestamp_sec) * 1000)

        return cls(
            pair=pair,
            price=price,
            volume=volume,
            timestamp=cls._milliseconds2datestr(timestamp_ms),
            timestamp_ms=timestamp_ms,
        )

    @classmethod
    def from_kraken_websocket_api_response(
        cls, pair: str, price: float, volume: float, timestamp_sec: int
    ) -> 'Trade':
        return cls(
            pair=pair,
            price=price,
            volume=volume,
            timestamp=datetime.fromtimestamp(timestamp_sec),
        )

    @staticmethod
    def _milliseconds2datestr(milliseconds: int) -> str:
        return datetime.fromtimestamp(milliseconds / 1000).strftime(
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )

    @staticmethod
    def _datestr2milliseconds(datestr: str) -> int:
        return int(
            datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp() * 1000
        )
