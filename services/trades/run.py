from loguru import logger
from src.kraken_api import KrakenApi
from quixtreams import Application


def main(
    kafka_broker_address: str,
    kafka_topic: str
):
    """
    Main function to start the trades service
    1 It reads the trades from the Kraken
    2 push them to the Kafka topic
    
    Args:
        kafka_broker_address: str
        kafka_topic: str
    Returns:
        None
    """
    logger.info("Strart trades service!")
    kraken_api = KrakenApi(pair="BTC/USD")
    
    while True:
        trades = kraken_api.get_trades(pair="BTC/USD")
        
        for trade in trades:
            # Create an Application instance with Kafka config
            app = Application(broker_address=kafka_broker_address)
            
            # Define a topic with JSON serialization
            topic = app.topic(name=kafka_topic, value_serializer='json')
            # Create a Producer instance
            with app.get_producer() as producer:
                while True:
                    trade = kraken_api.get_trades(pair="BTC/USD")
                    
                    for trade in trades:
                        message = topic.serialize(key=trade.pair, value=trade.to_dict())
                        producer.produce(topic=topic.name, value=message.value, key=message.key)
            
            logger.info(f"Pushed trade to kafka topic: {trade}")

if __name__ == "__main__":
    
    from config import config
    
    main(kafka_broker_address=config.kafka_broker_address, kafka_topic=config.kafka_topic)