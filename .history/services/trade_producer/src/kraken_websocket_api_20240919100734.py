from datetime import datetime, timezone
from typing import List
from websocket import create_connection
import json
from loguru import logger

from pydantic import BaseModel 



class KrakenWebsocketAPI:
    
    """
    Class for reading real time trades from the Kraken websocket API.
    """
    URL = 'wss://ws.kraken.com/v2'
    
    def __init__(self, product_id: str):
        """
        Initializes the KrakenWebsocketAPI instance
        
        Args:
            product_id (str): Product id of the trades to be read.
        """
        self.product_id = product_id
        
        # establish connection to the Kraken websocket API
        self._ws = create_connection(self.URL)
        logger.debug('Connection established')

        # subscribe to the trades for the given `product_id`
        self._subscribe(product_id)
        
    def _subscribe(self, product_id: str):
        """
        Establishes connection to the Kraken websocket API and subscribes to the trades for the given `product_id`.
        """
        looger.info(f"Subscribing to {product_id} trades")

        #let's subscribe to the trades for the given `product_id`
        msg={
            "method": "subscribe",
            "params": {
                "channel": "trade",
                "symbol": [
                    "ETH/EUR"
                ],
                "snapshot": false
            },
        }        

        self._ws.send(json.dumps(msg))
        logger.info(f'Subscribed successfully to {product_id} trades')
        # for each product_id we dump
        # the first two messages we got from the websocket, because they are not trades
        # they are just confirmation messages of the subscription
        for product_id in [product_id]:
            _ = self._ws.recv()
            _ = self._ws.recv()
    
    def get_trades(self) -> List[dict]:
        
        """
        Returns the latest batch of trades from the Kraken websocket API.
        """
        message = self._ws.recv()
        
        if "heartbeat" in message:
            "when we receive a heartbeat message, we just return an empty list"
            return []
        
        # otherwise parse the message
        message = json.loads(message)
        
        # extract the trade data
        trades = [ ]
        
        for trade in message["data"]:
            # extract the following fields
                # - product_id
                # - quantity
                # - price
                # - timestamp in milliseconds
                
            breackpoint()
            
            trades.append(
                Trade(
                product_id=self.product_id,
                price=float(trade[0]),
                qty=float(trade[1]),
                timestamp_ms=timestamp_ms,
                )
            )
            
        
        # Sleep for 1 second
        from time import sleep
        sleep(1)
        
        return event
     
    def is_done(self) -> bool:
        """
        Returns True if the API connection is closed and has no more trades to return.
        """
        False
        