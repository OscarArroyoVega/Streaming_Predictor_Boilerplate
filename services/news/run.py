from loguru import logger
from news_data_source import NewsDataSource
from news_downloader import NewsDownloader
from quixstreams import Application


def main(kafka_broker_address: str, kafka_topic: str, news_source: NewsDataSource):
    """ "
    1. Gets news from cryptopanic api
    2. Send it to kafka topic
    """
    logger.info(
        f'Starting news service with kafka broker address: {kafka_broker_address} and kafka topic: {kafka_topic}'
    )

    app = Application(broker_address=kafka_broker_address)

    output_topic = app.topic(name=kafka_topic, value_serializer='json')

    # create a streaming dataframe
    sdf = app.dataframe(source=news_source)

    # send the streaming dataframe to the output topic
    sdf = sdf.to_topic(output_topic)

    app.run()


if __name__ == '__main__':
    from config import config, cryptopanic_config
    from news_downloader import NewsDownloader

    # News Downloader object
    news_downloader = NewsDownloader(
        cryptopanic_api_key=cryptopanic_config.cryptopanic_api_key
    )

    # News Data Source object
    news_source = NewsDataSource(
        news_downloader, polling_interval_seconds=config.polling_interval_sec
    )

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        news_source=news_source,
    )
