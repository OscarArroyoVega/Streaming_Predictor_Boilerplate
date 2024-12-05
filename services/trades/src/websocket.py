from typing import List
from websocket import create_connection
import json
from .trade import Trade
from loguru import logger

class KrakenWebsocketApi:
    """
    Websocket client for connecting to Kraken's real-time trade data API.
    """ 
    
    URL = "wss://ws.kraken.com/v2"
    def __init__(self, pairs: List[str]):
        self.pairs = pairs
        
        # create a connection to the websocket
        self._ws_client = create_connection(self.URL)
        
        #create a subscription to the websocket 
        self._subscribe()
    

    def get_trade_data(self) -> List[Trade]:
        """
        Fetch the trade data from the Kraken websocket APIs and return a list of Trade objects
        """
        logger.info(f"Fetching trade data for pairs: {self.pairs}")
        
        # Keep reading messages until we get trade data
        while True:
            data = self._ws_client.recv()
            data_dict = json.loads(data)
            
            # Skip heartbeat messages
            if data_dict.get('channel') == 'heartbeat':
                logger.info("HEARTBEAT")
                continue
            
            # Check if the message contains trade data
            if 'data' in data_dict:
                trade_data = data_dict["data"]
                break
            else:
                logger.warning("Received message without trade data")
                continue
                
        trades = [Trade(
            pair=trade["symbol"],
            price=trade["price"],
            volume=trade["qty"],
            timestamp=trade["timestamp"],
            ) for trade in trade_data]

        return trades

    def _subscribe(self):
        """
        Subscribe to the websocket and receive messages
        """
        self._ws_client.send(   
            json.dumps({
                "method": "subscribe",
                "params": {
                    "channel": "trade",
                    "symbol": self.pairs,
                    "snapshot": True
                }
            })
        )
        
        for pair in self.pairs:
            _ = self._ws_client.recv()
            _ = self._ws_client.recv()
            
        
        
