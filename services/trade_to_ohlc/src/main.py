from quixstreams import Application
from datetime import timedelta

from loguru import logger


def init_ohlc_candle(trade: dict):
    """
    Returns the initial OHLC candle when the first `trade` in that window happens.
    """
    return {
        'open': trade['price'],
        'high': trade['price'],
        'low': trade['price'],
        'close': trade['price'],
        'volume': trade['quantity'],
        'product_id': trade['product_id'],
    }

def update_ohlc_candle(candle: dict, trade: dict):
    """
    Updates the OHLC candle with the new `trade`.
    """
    candle['high'] = max(candle['high'], trade['price'])
    candle['low'] = min(candle['low'], trade['price'])
    candle['close'] = trade['price']
    candle['volume'] += trade['quantity']
    candle['product_id'] = trade['product_id']
    # candle['timestamp_ms'] = trade['timestamp_ms']
    return candle  # TODO add open to candle as candle['open'] = trade['price']**before update_ohlc_candle() 

def transform_trade_to_ohlcv(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    ohlcv_window_seconds: int,
    ):
    """
    Reads incoming trades from a Kafka topic, aggregates them into OHLC data and writes the OHLC data to another Kafka topic.
    
    Args:
        kafka_broker_address (str): The address of the Kafka broker.
        kafka_input_topic (str): The name of the Kafka topic to read trades from.
        kafka_output_topic (str): The name of the Kafka topic to write OHLC data to.
        product_consumer_group (str): The name of the Kafka consumer group.
        
    Returns:
        None
    """
    
    # Define the application with Redpanda broker address
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
)

    # Define the input and output topics
    input_topic = app.topic(name=kafka_input_topic, value_deserializer="json")
    output_topic = app.topic(name=kafka_output_topic, value_serializer="json")

    # Create a StreamingDataFrame for the input topic
    sdf = app.dataframe(input_topic)
    
    # debug for incoming messages
    #sdf.update(logger.debug)

    # Apply processing logic
    #sdf = sdf.update(lambda row: {"processed_value": row["original_value"] * 2})

    # Send the processed data to the output topic
    #sdf = sdf.to_topic(output_topic)
    

    # create the application window, the meat of the application
    sdf = (
        sdf.tumbling_window(duration_ms=timedelta(seconds=ohlcv_window_seconds))
        .reduce(
            reducer=update_ohlc_candle,
            initializer=init_ohlc_candle,)
        .final()
    )
    
    # unpack the dictionary into separate columns
    sdf["open"] = sdf["value"]["open"]
    sdf["high"] = sdf["value"]["high"]
    sdf["low"] = sdf["value"]["low"]
    sdf["close"] = sdf["value"]["close"]
    sdf["volume"] = sdf["value"]["volume"]
    sdf["timestamp_ms"] = sdf["end"]
    
    # keep only the columns we need
    sdf = sdf[["timestamp_ms", "open", "high", "low", "close", "volume"]]
    
    #print the output to the console
    sdf.update(logger.debug)
    
    sdf = sdf.to_topic(output_topic)
    
    # Run or kick off the application
    app.run(sdf)
    

if __name__ == "__main__":
    transform_trade_to_ohlcv(
        kafka_broker_address="localhost:19092",
        kafka_input_topic="trade",
        kafka_output_topic="ohlcv", # FIXME extract config info to environment variables file
        kafka_consumer_group="consumer_group_trade_to_ohlcv_2",
        ohlcv_window_seconds=60,
        
    )                   

    