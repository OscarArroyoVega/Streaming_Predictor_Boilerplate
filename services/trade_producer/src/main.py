from typing import List

from loguru import logger
from quixstreams import Application

from src.kraken_websocket_api import (
    KrakenWebsocketAPI,
    Trade,
)

def produce_trades(
    kafka_broker_address: str,
    kafka_topic: str,
    trade_data_source: TradeSource,
    product_id: str,
):
    """
    Reads trades from the Kraken websocket API and saves them the given Kafka topic.
    
    Args:
        kafka_broker_address (str): Kafka broker address.
        kafka_topic (str): Kafka topic where the trades will be saved.
        product_id (str): Product id of the trades to be saved.
        
    Returns:    
        None
    """
    
    # Create an Application to connect to the Quix broker with kafka topic
    app = Application(broker_address=kafka_broker_address)
    
    # Define an output topic with JSON serialization
    topic = app.topic(name=kafka_topic, value_serializer='json')
    
    # Create an instance of the KrakenWebsocketAPI class
    kraken_api = KrakenWebsocketAPI(product_id=product_id)
    

    # Create a Producer instance
    with app.get_producer() as producer:
        
        while True:
            trades: List[Trade] = kraken_api.get_trades()
            
            for trade in trades:
                # Serialize the trade using the defin000000000d topic 
                # Transform it into a sequence of bytes
                message = topic.serialize(key=trade.product_id, value=trade.model_dump())
                
                # Produce the message into the kafka topic
                producer.produce(topic=topic.name, key=message.key, value=message.value)
                
                #affter producing the trade, log the trade
                logger.debug(f"Pushed trade to Kafka: {trade}")


    
if __name__ == "__main__":
    
    from src.config import config

    if config.live_or_historical == 'live':
        from src.trade_data_source.kraken_websocket_api import KrakenWebsocketAPI
        kraken_api = KrakenWebsocketAPI(product_id=config.product_id)
    
    elif config.live_or_historical == 'historical':
        from src.trade_data_source.kraken_rest_api import KrakenRestAPI
        kraken_api = KrakenRestAPI(
            product_id=config.product_id,
            last_n_days=config.last_n_days,
        )
    else:
        raise ValueError('Invalid value for `live_or_historical`')
    
    produce_trades(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        trade_data_source=kraken_api,
    )