from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_consumer_group: str,
    feature_group_name: str,
    feature_group_version: int,
):
    """
    Main function to run the to-feature-store service.
    1. Read messages from kafka and push them to the feature store.
    2. Push the messages to the feature group.
    """

    app = Application(
        broker_address=kafka_broker_address, consumer_group=kafka_consumer_group
    )
    input_topic = app.add_topic(kafka_input_topic, value_deserializer='json')

    logger.info('Starting to-feature-store service!')

    return input_topic


if __name__ == '__main__':
    from config import config, hopsworks_credentials

    main(
        api_key=hopsworks_credentials.hopsworks_api_key,
        project_name=hopsworks_credentials.hopsworks_project_name,
        api_url=hopsworks_credentials.hopsworks_api_url,
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
    )
