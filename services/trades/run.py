from kraken_api.base import TradesAPI
from kraken_api.mock import KrakenMockAPI
from kraken_api.rest import KrakenRestAPI
from kraken_api.websocket import KrakenWebsocketApi
from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    trades_api: TradesAPI,
):
    """
    Main function to start the trades service
    1 It reads the trades from the Kraken
    2 push them to the Kafka topic using the provided API

    Args:
        kafka_broker_address: str
        kafka_topic: str
        kraken_api: TradesAPI
    Returns:
        None
    """
    logger.info('Start trades service!')

    # Create an Application instance with Kafka config
    app = Application(
        broker_address=kafka_broker_address,
    )

    # define topic
    topic = app.topic(name=kafka_topic, value_serializer='json')

    # Create a Producer instance
    with app.get_producer() as producer:
        while not trades_api.is_done():
            logger.info('Getting trades from Kraken')
            trades = trades_api.get_trade_data()

            for trade in trades:
                trade = trade.to_dict()
                logger.debug(f'trade: {trade}')
                message = topic.serialize(key=trade['pair'], value=trade)
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f'Pushed trade to kafka topic: {trade}')


if __name__ == '__main__':
    from config import config

    if config.data_source == 'live':
        kraken_api = KrakenWebsocketApi(pairs=config.pairs)
    elif config.data_source == 'historical':
        kraken_api = KrakenRestAPI(pairs=config.pairs, last_n_days=config.last_n_days)
    elif config.data_source == 'test':
        kraken_api = KrakenMockAPI(pairs=config.pairs)
    else:
        raise ValueError(f'Invalid mode: {config.data_source}')

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        trades_api=kraken_api,
    )
