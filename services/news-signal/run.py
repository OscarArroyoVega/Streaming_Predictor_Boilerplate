from llms.base import BaseNewsSignalExtractor
from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    llm: BaseNewsSignalExtractor,
):
    logger.info('Hello from news-signal!')

    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
        auto_offset_reset='earliest',
    )

    input_topic = app.topic(
        name=kafka_input_topic,
        value_deserializer='json',
    )

    output_topic = app.topic(
        name=kafka_output_topic,
        value_serializer='json',
    )

    sdf = app.dataframe(input_topic)

    def process_news_signal(value: dict, llm: BaseNewsSignalExtractor) -> dict:
        logger.debug(f'Processing value: {value}')
        try:
            news_title = value.get('title', '')
            logger.debug(f'News title: {news_title}')
            signal = llm.get_signal(news_title)
            logger.debug(f'Signal: {signal}')
            return {
                'news': news_title,
                'model_name': llm.model_name,
                'timestamp_ms': value['timestamp_ms'],
                **signal,
            }
        except Exception as e:
            logger.error(f'Error processing news signal: {str(e)}')
            raise

    # Use the function in the dataframe transformation
    sdf = sdf.apply(lambda value: process_news_signal(value, llm))

    sdf = sdf.update(lambda value: logger.debug(f'Final message: {value}'))

    sdf = sdf.to_topic(output_topic)

    app.run()


if __name__ == '__main__':
    from config import config
    from llms.factory import get_llm

    logger.info(f'Using model provider: {config.model_provider}')
    llm = get_llm(config.model_provider)

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        llm=llm,
    )