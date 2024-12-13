from datetime import datetime
from typing import List, Tuple

import requests
from loguru import logger
from pydantic import BaseModel


class News(BaseModel):
    """
    this is the data model for the news
    """

    title: str
    published_at: datetime
    domain: str
    # url: str
    # TODO also pick the URL and expand the context to feed the LLM


class NewsDownloader:
    URL = 'https://cryptopanic.com/api/v1/posts/'

    def __init__(self, cryptopanic_api_key: str):
        self.cryptopanic_api_key = cryptopanic_api_key
        # logger.debug(f"Cryptopanic API key: {self.cryptopanic_api_key}")
        # self._last_published_at = None

    def get_news(self) -> List[News]:
        """
        this is the main function that gets the news, keeeps on calling the API until it gets no new more news
        """
        news = []
        url = self.URL + '?auth_token=' + self.cryptopanic_api_key
        while url:
            logger.debug(f'Fetching news from {url}')
            batch_of_news, next_url = self._get_batch_of_news(url)
            news += batch_of_news
            logger.debug(f'Fetched {len(batch_of_news)} news')
            if not batch_of_news:
                break
            logger.debug(f'Total news fetched: {len(news)}')
            url = next_url

        # sort the news by published_at
        news.sort(key=lambda x: x.published_at, reverse=False)

        return news

    def _get_batch_of_news(self, url: str) -> Tuple[List[News], str]:
        """
        Connects to Cryptopanic API and fetches news

        Args:
            url: the URL to fetch the news from

        Returns:
            a tuple containing the news and the next URL to fetch the news from
        """
        response = requests.get(url)
        try:
            response = response.json()
        except Exception as e:
            logger.error(f'Error fetching news: {e}')
            from time import sleep

            sleep(1)
            return ([], '')

        news = [
            News(
                title=post['title'],
                published_at=post['published_at'],
                domain=post['domain'],
            )
            for post in response['results']
        ]

        # get the next URL
        next_url = response['next']

        return news, next_url


if __name__ == '__main__':
    from config import config

    cryptopanic_api_key = config.cryptopanic_api_key

    news_downloader = NewsDownloader(cryptopanic_api_key)
    news = news_downloader.get_news()
