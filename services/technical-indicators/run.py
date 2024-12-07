from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    num_candles_in_state: int,
):
    """
    Main function to start the technical-indicators service. 3 steps:
    1. Ingress candles from the candles service into the technical-indicators service using a Kafka consumer group
    2. Computes technical indicators based on the candles
    3. Outputs the technical indicators to a Kafka topic

    Args:
        kafka_broker_address: The address of the Kafka broker
        kafka_input_topic: The topic to consume candles from
        kafka_output_topic: The topic to output technical indicators to
        kafka_consumer_group: The consumer group to use for the Kafka consumer
        num_candles_in_state: The number of candles to keep in the state

    Returns:
        None
    """
    logger.info('Starting technical-indicators service...')

    app = Application(
        broker_address=kafka_broker_address, consumer_group=kafka_consumer_group
    )

    input_topic = app.topic(name=kafka_input_topic, value_deserializer='json')
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    sdf = app.dataframe(topic=input_topic)
    sdf = sdf.update(lambda value: logger.info(f'Candle: {value}'))
    sdf = sdf.to_topic(output_topic)

    app.run()


if __name__ == '__main__':
    from config import config

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        num_candles_in_state=config.num_candles_in_state,
    )
