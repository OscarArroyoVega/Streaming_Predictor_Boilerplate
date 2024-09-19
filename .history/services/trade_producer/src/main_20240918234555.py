from loguru imoport logger

from quixstreams import Application
from src.kraken_websocket_api import KrakenWebsocketAPI

def produce_trade(
    kafka_broker_address: str,
    kafka_topic: str,
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
            trades = kraken_api.get_trades()
            
            for trade in trades:
                # Serialize the trade using the defined topic 
                # Transform it into a sequence of bytes
                message = topic.serialize(key=trade["product_id"], value=trade)
                
                # Produce the message into the kafka topic
                producer.produce(topic=topic.name, key=message.key, value=message.value)
                
                #affter producing the trade, log the trade
                logger.debug(f"Pushed trade to Kafka: {trade}")


        
if __name__ == '__main__':
    produce_trade(
        kafka_broker_address='localhost:19092',
        kafka_topic='trade',
        product_id='ETH/EUR',
    )