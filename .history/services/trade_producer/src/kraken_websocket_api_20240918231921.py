from typing import List

class KrakenWebsocketAPI:
    
    """
    Class for reading real time trades from the Kraken websocket API.
    """
    
    def __init__(self, product_id: str):
        """
        Initializes the KrakenWebsocketAPI instance
        
        Args:
            product_id (str): Product id of the trades to be read.
        """
        self.product_id = product_id

    def get_trades(self): -> List[dict]:
        """
        Returns the latest batch of trades from the Kraken websocket API.
        """
        event = [{
            "product_id": "ETH/EUR", 
            "price": 1000,
            "qty": 1,
            "timestamp_ms": 1609459200000,
        }]
        
        return event
     
    def is_done(self) -> bool:
        """
        Returns True if the API connection is closed and has no more trades to return.
        """
        False
        