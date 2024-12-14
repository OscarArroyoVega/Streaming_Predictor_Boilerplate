from datetime import datetime
from time import sleep
from typing import Optional

from loguru import logger
from news_downloader import NewsDownloader
from quixstreams.sources.base import StatefulSource


class NewsDataSource(StatefulSource):
    def __init__(
        self,
        news_downloader: NewsDownloader,
        polling_interval_seconds: Optional[int] = 0,
    ):
        """
        Initialize the NewsDataSource
        """
        super().__init__(name='news_data_source')

        self.news_downloader = news_downloader
        self.polling_interval_seconds = polling_interval_seconds

    def run(self):
        """
        this is the main function that fetches news from Cryptopanic API
        """
        last_published_at_str = self.state.get('last_published_at', None)
        if last_published_at_str is not None:
            last_published_at = datetime.fromisoformat(last_published_at_str)
        else:
            last_published_at = None

        while self.running:
            # download news
            # ATTENTION: the news are in ascending order of published_at
            news = self.news_downloader.get_news()

            # keep only the news that are not duplicates (be aware of ascending order or descending order of published_at)
            if last_published_at is not None:
                news = [
                    news_item
                    for news_item in news
                    if news_item.published_at > last_published_at
                ]
                logger.debug(
                    f'Filtered news items with published_at > {last_published_at}'
                )
            logger.debug(f'Number of news after filtering: {len(news)}')

            # produce the news
            for news_item in news:
                # serialize the news item in bytes
                serialized_news_item = self.serialize(
                    key='news', value=news_item.to_dict()
                )
                # produce the news to the kafka topic
                self.produce(
                    key=serialized_news_item.key, value=serialized_news_item.value
                )
                logger.debug(
                    f'Produced news item with published_at={news_item.published_at}'
                )
            # update the last published at
            if news:
                last_published_at = news[-1].published_at

            # update the state
            self.state.set('last_published_at', last_published_at.isoformat())

            # flush the state changes
            self.flush()

            # slow down mechanism
            sleep(self.polling_interval_seconds)
