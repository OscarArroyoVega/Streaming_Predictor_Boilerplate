from typing import Literal

from loguru import logger
from quixstreams import Application
from sinks import HopsworksSink


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_consumer_group: str,
    output_sink: HopsworksSink,
    data_source: Literal['live', 'historical'],
):
    """
    Main function to run the to-feature-store service.
    1. Read messages from kafka and push them to the feature store.
    2. Push the messages to the feature group.
    Args:
        kafka_broker_address: The address of the Kafka broker
        kafka_input_topic: The topic to consume messages from
        kafka_consumer_group: The consumer group to use for the Kafka consumer
        output_sink: The sink to write the messages to
        data_source: The data source to use for the to-feature-store service
    """
    logger.info('Starting to-feature-store service!')

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
        auto_offset_reset='earliest' if data_source == 'historical' else 'latest',
    )

    # Clear the state before starting in historical pipeline
    if data_source == 'historical':
        logger.info('Clearing application state...')
        try:
            app.clear_state()
            logger.info('Application state cleared!')
        except FileNotFoundError:
            logger.info('No state directory found to clear. Continuing...')

    input_topic = app.topic(kafka_input_topic, value_deserializer='json')

    # Read the data from the input topic
    sdf = app.dataframe(input_topic)

    # Write the data to the output sink
    sdf.sink(output_sink)
    logger.info('Data written to the feature store!')

    # Start the application
    app.run()


if __name__ == '__main__':
    from config import config, hopsworks_credentials

    # Sink settings to write data to the feature store
    hopsworks_sink = HopsworksSink(
        # Hopsworks credentials
        api_key=hopsworks_credentials.hopsworks_api_key,
        project_name=hopsworks_credentials.hopsworks_project_name,
        # Feature group settings
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
        feature_group_primary_keys=config.feature_group_primary_keys,
        feature_group_event_time=config.feature_group_event_time,
        feature_group_materialization_minutes=config.feature_group_materialization_minutes,
    )

    main(
        # Kafka settings
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        # Output sink settings
        output_sink=hopsworks_sink,
        data_source=config.data_source,
    )
