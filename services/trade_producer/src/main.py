from typing import List

from loguru import logger
from quixstreams import Application
from quixstreams.models import TopicConfig

# from src.trade_data_source.kraken_websocket_api import (
#     KrakenWebsocketAPI,
#     Trade,
# )

# from src.trade_data_source import (
#     Trade,
#     TradeSource,
# )
# breakpoint()

# from src.trade_data_source.trade import Trade
# from src.trade_data_source.base import TradeSource
from src.trade_data_source import Trade, TradeSource

def produce_trades(
    kafka_broker_address: str,
    kafka_topic: str,
    trade_data_source: TradeSource,
    num_partitions: int,
):
    """
    Reads trades from the Kraken Websocket API and saves them in the given `kafka_topic`

    Args:
        kafka_broker_address (str): The address of the Kafka broker
        kafka_topic (str): The Kafka topic to save the trades
        trade_data_source (TradeSource): The data source to get the trades from
        num_partitions (int): The number of partitions to create for the Kafka topic

    Returns:
        None
    """    
    # Create an Application instance with Kafka config
    app = Application(broker_address=kafka_broker_address)

    # Define a topic "my_topic" with JSON serialization
    topic = app.topic(
        name=kafka_topic, 
        value_serializer='json',
        config=TopicConfig(
            num_partitions=num_partitions,
            replication_factor=1
        )
    )

    # Create a Producer instance
    with app.get_producer() as producer:

        while not trade_data_source.is_done():
        # while trade_data_source.is_done() is False:

            trades: List[Trade] = trade_data_source.get_trades()
            
            # breakpoint()

            for trade in trades:
                # Serialize an event using the defined Topic
                # transform it into a sequence of bytes
                message = topic.serialize(
                    key=trade.product_id.replace('/','-'),
                    value=trade.model_dump()
                )

                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name, 
                    value=message.value, 
                    key=message.key
                )

                # logger.debug(f'Message key: {message.key}')
                
                logger.debug(f"Pushed trade to Kafka: {trade}")

        #breakpoint()


if __name__ == "__main__":
    
    from src.config import config

    if config.live_or_historical == 'live':
        from src.trade_data_source.kraken_websocket_api import KrakenWebsocketAPI
        kraken_api = KrakenWebsocketAPI(product_ids=config.product_ids)
    
    elif config.live_or_historical == 'historical':
        from src.trade_data_source.kraken_rest_api import KrakenRestAPI
        kraken_api = KrakenRestAPI(
            product_ids=config.product_ids,
            last_n_days=config.last_n_days,
        )
    else:
        raise ValueError('Invalid value for `live_or_historical`')
                         
    produce_trades(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        trade_data_source=kraken_api,
        num_partitions=len(config.product_ids),
    )