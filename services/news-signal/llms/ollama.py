import json
from typing import Literal, Optional

from llama_index.core.prompts import PromptTemplate
from llama_index.llms.ollama import Ollama
from loguru import logger

from .base import BaseNewsSignalExtractor, NewsSignal


class OllamaNewsSignalExtractor(BaseNewsSignalExtractor):
    def __init__(
        self,
        model_name: str,
        temperature: Optional[float] = 0,
        timeout: float = 120.0,
        max_retries: int = 3,
    ):
        self.llm = Ollama(model=model_name, temperature=temperature, timeout=timeout)

        self.prompt_template = PromptTemplate(
            template="""You are a cryptocurrency market analyst. Analyze this news article and provide signals for BTC and ETH prices.

            Article: {news_article}

            Rules:
            1. Signal values must be EXACTLY one of these integers:
            - 1  (BULLISH: positive impact)
            - 0  (NEUTRAL: no significant impact)
            -1  (BEARISH: negative impact)

            2. Provide a brief, factual reasoning (max 150 characters)
            3. Return only a JSON object with this exact structure:
            {
                "btc_signal": Literal[-1, 0, 1],  # -1=bearish, 0=neutral, 1=bullish
                "eth_signal": Literal[-1, 0, 1],  # -1=bearish, 0=neutral, 1=bullish
                "reasoning": "string"
            }

            Example response:
            {
                "btc_signal": 1,
                "eth_signal": 0,
                "reasoning": "Bitcoin ETF approval news directly impacts BTC market sentiment, while having minimal effect on ETH"
            }
            """
        )

        self.model_name = model_name
        self.max_retries = max_retries

    def get_signal(
        self, text: str, output_format: Literal['dict', 'NewsSignal'] = 'dict'
    ) -> NewsSignal | dict:
        for attempt_num in range(self.max_retries):
            try:
                # Get raw response from LLM
                response = self.llm.complete(
                    prompt=self.prompt_template.format(news_article=text)
                )
                logger.debug(f'Response: {response}')
                # Parse the response text as JSON
                response_dict = json.loads(response.text)
                logger.debug(f'Response dict: {response_dict}')
                # Create NewsSignal object
                news_signal = NewsSignal(
                    btc_signal=response_dict['btc_signal'],
                    eth_signal=response_dict['eth_signal'],
                    reasoning=response_dict['reasoning'],
                )

                if output_format == 'dict':
                    return news_signal.to_dict()
                return news_signal

            except (json.JSONDecodeError, KeyError) as e:
                raise ValueError(f'Failed to parse LLM response: {str(e)}') from e

            except Exception as e:
                if attempt_num < self.max_retries - 1:
                    logger.warning(
                        f'Timeout on attempt {attempt_num + 1}/{self.max_retries}, retrying...'
                    )
                logger.error(f'Unexpected error: {str(e)}')
                raise


if __name__ == '__main__':
    from .config import OllamaConfig

    config = OllamaConfig()

    llm = OllamaNewsSignalExtractor(
        model_name=config.llm_name,
        timeout=120.0,
        max_retries=3,
    )

    examples = [
        "Bitcoin ETF ads spotted on China's Alipay payment app",
        "U.S. Supreme Court Lets Nvidia's Crypto Lawsuit Move Forward",
        "Trump's World Liberty Acquires ETH, LINK, and AAVE in $12M Crypto Shopping Spree",
    ]

    for example in examples:
        try:
            logger.info(f'Example: {example}')
            signal = llm.get_signal(example)
            logger.info(f'Signal after processing get_signal: {signal}')
        except TypeError as e:
            logger.error(f'Error: {e}')

    """
    Example: Bitcoin ETF ads spotted on China’s Alipay payment app
    {
        "btc_signal": 1,
        "eth_signal": 0,
        'reasoning': "The news of Bitcoin ETF ads being spotted on China's Alipay payment
        app suggests a growing interest in Bitcoin and other cryptocurrencies among Chinese
        investors. This could lead to increased demand for BTC, causing its price to rise."
    }

    Example: U.S. Supreme Court Lets Nvidia’s Crypto Lawsuit Move Forward
    {
        'btc_signal': -1,
        'eth_signal': -1,
        'reasoning': "The US Supreme Court's decision allows Nvidia to pursue its crypto
        lawsuit, which could lead to increased regulatory uncertainty and potential
        restrictions on cryptocurrency mining. This could negatively impact the prices
        of both BTC and ETH."
    }

    Example: Trump’s World Liberty Acquires ETH, LINK, and AAVE in $12M Crypto Shopping Spree
    {
        'btc_signal': 0,
        'eth_signal': 1,
        'reasoning': "The acquisition of ETH by a major company like
        Trump's World Liberty suggests that there is increased demand for
        Ethereum, which could lead to an increase in its price."
    }
    """
