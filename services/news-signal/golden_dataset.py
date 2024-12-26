import json
import random
from typing import Literal

import pandas as pd
from llms.factory import get_llm
from loguru import logger
from tqdm import tqdm

instruction = """
    You are an expert crypto financial analyst with deep knowledge of market dynamics and sentiment analysis.
    Analyze the following news story and determine its potential impact on crypto asset prices.
    Focus on both direct mentions and indirect implications for each asset.

    Do not output data for a given coin if the news is not relevant to it.

    ## Example input
    "Goldman Sachs wants to invest in Bitcoin and Ethereum, but not in XRP"

    ## Example output
    [
        {"coin": "BTC", "signal": 1},
        {"coin": "ETH", "signal": 1},
        {"coin": "XRP", "signal": -1},
    ]

    News story to analyze:
    {news_story}
    """

input_file = './data/cryptopanic_news.csv'


def generate_dataset(
    model_provider: Literal['anthropic', 'ollama'],
    output_file: str,
    num_samples: int = 1000,
) -> list[dict]:
    """
    Generate a golden dataset with (instruction, input, output) tuples to do
    Supervised Fine Tuning
    Args:
        model_provider: The model provider to use for generating the dataset
        output_file: The file to write the dataset to
        num_samples: The number of samples to generate
        input_file: The file to read the news from
    Returns:
        None
    """

    df = pd.read_csv(input_file)
    news = df['title'].tolist()
    # randomly sample 1000 news
    news = random.sample(news, num_samples)
    # llm config
    llm = get_llm(model_provider=model_provider)
    for news_item in tqdm(news):
        try:
            signals = llm.get_signal(news_item)
            output = {
                'instruction': instruction,
                'input': news_item,
                'output': signals.model_dump_json(),
                'model_name': llm.model_name,
            }

        except Exception as e:
            logger.error(f'Error generating signal for news item: {news_item}')
            logger.exception(e)
            continue

        with open(output_file, 'a') as f:
            f.write(json.dumps(output) + '\n')


if __name__ == '__main__':
    from fire import Fire

    Fire(generate_dataset)
