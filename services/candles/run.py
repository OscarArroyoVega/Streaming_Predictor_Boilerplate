from datetime import timedelta
from typing import Any, List, Optional, Tuple

from loguru import logger
from quixstreams import Application
from quixstreams.models import TimestampType

# Custom timestamp extractor for the input topic (to ensure the timestamp is in milliseconds)


def custom_ts_extractor(
    value: Any,
    headers: Optional[List[Tuple[str, bytes]]],
    timestamp: float,
    timestamp_type: TimestampType,
) -> int:
    """
    Custom timestamp extractor for the input topic (to ensure the timestamp is in milliseconds)
    Args:
        value (Any): The value of the incoming message.
        headers (Optional[List[Tuple[str, bytes]]]): The headers of the incoming message.
        timestamp (float): The timestamp of the incoming message.
        timestamp_type (int): The type of the timestamp.
    Returns:
        int: The timestamp in milliseconds.
    """
    return value['timestamp_ms']


def init_candle(trade: dict) -> dict:
    """
    Initialize a candle with the first trade
    """
    return {
        'open': trade['price'],  # open is the same as the price for the first trade
        'high': trade['price'],  # high is the same as the price for the first trade
        'low': trade['price'],  # low is the same as the price for the first trade
        'close': trade['price'],  # close is the same as the open for the first trade
        'volume': trade['volume'],  # volume is the same as the size for the first trade
        'timestamp_ms': trade['timestamp_ms'],
        'pair': trade['pair'],
    }


def update_candle(candle: dict, trade: dict) -> dict:
    """
    Update the candle with the new trade
    """
    return {
        'open': candle['open'],
        'high': max(candle['high'], trade['price']),
        'low': min(candle['low'], trade['price']),
        'close': trade['price'],
        'volume': candle['volume'] + trade['volume'],
        'timestamp_ms': trade['timestamp_ms'],
        'pair': trade['pair'],
    }


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_interval_seconds: int,  # TODO add many other services for other intervals (1hour, 15minutes, 1 day...)
    emit_incomplete_candles: bool,
):
    """
    Main function to run the candles service.
    3 steeps
    1. ingest data from kafka topic
    2. calculate candles, generate them with tumbling window (candle_interval_seconds)
    3. Output candles to kafka topic

    Args:
        kafka_broker (_type_, optional): Defaults to config.kafka_broker.
        kafka_input_topic (_type_, optional): Defaults to config.kafka_input_topic.
        kafka_output_topic (_type_, optional): Defaults to config.kafka_output_topic.
        kafka_consumer_group (_type_, optional): Defaults to config.kafka_consumer_group.
        candle_interval_seconds (_type_, optional): Defaults to config.candle_interval_seconds.

    Returns:
        None
    """
    logger.info(
        f'Hello from candles service! {kafka_broker_address} {kafka_input_topic} {kafka_output_topic} {kafka_consumer_group} {candle_interval_seconds} '
    )

    # Initialize application
    app = Application(
        broker_address=kafka_broker_address, consumer_group=kafka_consumer_group
    )

    # Define input topic
    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer='json',
        timestamp_extractor=custom_ts_extractor,
    )

    # Define output topic
    output_topic = app.topic(
        name=kafka_output_topic,
        value_serializer='json',
    )

    # create dataframe from the input topic
    sdf = app.dataframe(topic=input_topic)

    # Agregation Trades into candles using tumbling windows
    # 1. define tumbling window
    sdf = sdf.tumbling_window(timedelta(seconds=candle_interval_seconds))
    # 2. define the reduce operation or initial value with the first trade
    sdf = sdf.reduce(reducer=update_candle, initializer=init_candle)
    # 3. emit all the intermediate results to have more granularity
    if emit_incomplete_candles:
        sdf = sdf.current()

    else:
        sdf = sdf.final()

    # extract open, high, low, close, volume, timestamp_ms, pair from the dataframe
    sdf['open'] = sdf['value']['open']
    sdf['high'] = sdf['value']['high']
    sdf['low'] = sdf['value']['low']
    sdf['close'] = sdf['value']['close']
    sdf['volume'] = sdf['value']['volume']
    sdf['timestamp_ms'] = sdf['value']['timestamp_ms']
    sdf['pair'] = sdf['value']['pair']

    sdf['window_start'] = sdf['start']
    sdf['window_end'] = sdf['end']

    sdf = sdf[
        [
            'pair',
            'timestamp_ms',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'window_start',
            'window_end',
        ]
    ]

    # print the value
    sdf = sdf.update(
        lambda value: logger.info(f'candle {candle_interval_seconds} seconds: {value}')
    )

    # push the candle to the output topic
    sdf = sdf.to_topic(output_topic)

    # run the application
    app.run()


if __name__ == '__main__':
    from config import config

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        candle_interval_seconds=config.candle_interval_seconds,
        emit_incomplete_candles=config.emit_incomplete_candles,
    )
