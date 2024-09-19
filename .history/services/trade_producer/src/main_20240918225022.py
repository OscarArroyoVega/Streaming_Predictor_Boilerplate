from quixstreams import Application

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
    output_topic = app.topic(name=kafka_topic, value_serializer='json')

    # Create a Producer instance
    with app.get_producer() as producer:
        
        while True:
            event = {"product_id": "ETH/EUR", 
                    "price": 1000,
                    "qty": 1,
                    "timestamp_ms": 1609459200000}
            # Serialize the event using the defined topic 
            # Transform it into a sequence of bytes
            message = output_topic.serialize(key=event["product_id"], value=event)
            
            #Produce the messageinto the kafka topic
            producer.produce(topic=output_topic.name, key=message.key, value=message.value)
            
            from time import sleep
            sleep(1)
        
if __name__ == '__main__':
    produce_trade(
        kafka_broker_address='localhost:19092',
        kafka_topic='trade',
        product_id='ETH/EUR',
    )