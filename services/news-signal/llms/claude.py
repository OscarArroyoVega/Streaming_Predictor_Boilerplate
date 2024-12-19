from typing import Literal, Optional

from llama_index.core.prompts import PromptTemplate
from llama_index.llms.anthropic import Anthropic
from loguru import logger

from .base import BaseNewsSignalExtractor, NewsSignal


class ClaudeNewsSignalExtractor(BaseNewsSignalExtractor):
    def __init__(
        self,
        model_name: str,
        api_key: str,
        temperature: Optional[float] = 0,
    ):
        self.llm = Anthropic(
            model=model_name,
            api_key=api_key,
            temperature=temperature,
        )

        self.prompt_template = PromptTemplate(
            template="""
            You are an expert crypto financial analyst with deep knowledge of market dynamics and sentiment analysis.
            Analyze the following news story and determine its potential impact on crypto asset prices.

            Rules:
            1. Output signal values:
            - 1 for positive impact (price likely to increase)
            - -1 for negative impact (price likely to decrease)
            - Do not output anything for coins not mentioned or impacted

            2. Consider both direct and indirect impacts:
            - Direct: "Bitcoin falls 5%" -> {"coin": "BTC", "signal": -1}
            - Indirect: "Fed raises rates" -> {"coin": "BTC", "signal": -1} (due to risk-off sentiment)

            3. Look for price-moving events like:
            - Major price movements
            - Market sentiment shifts
            - Regulatory news
            - Institutional adoption
            - Technical developments

            Example input: "Bitcoin drops below $40k as market sentiment turns bearish"
            Example output: [{"coin": "BTC", "signal": -1}]

            Be strict with your output.
            News story to analyze:
            {news_story}
            """
        )

        self.model_name = model_name

    def get_signal(
        self,
        text: str,
        output_format: Literal['dict', 'NewsSignal'] = 'NewsSignal',
    ) -> NewsSignal | dict:
        try:
            response: NewsSignal = self.llm.structured_predict(
                NewsSignal,
                prompt=self.prompt_template,
                news_story=text,
            )
            logger.debug(f'Claude response: {response}')

            # keep only news signals with non-zero signal
            response.news_signals = [
                news_signal
                for news_signal in response.news_signals
                if news_signal.signal != 0
            ]
            logger.debug(f'Filtered signals: {response.news_signals}')
            if output_format == 'dict':
                return response.to_dict()
            else:
                return response
        except Exception as e:
            logger.error(f'Error in signal extraction: {str(e)}')
            raise


if __name__ == '__main__':
    from .config import AnthropicConfig

    config = AnthropicConfig()

    llm = ClaudeNewsSignalExtractor(
        model_name=config.model_name,
        api_key=config.api_key,
    )

    examples = [
        "Bitcoin ETF ads spotted on China's Alipay payment app",
        "U.S. Supreme Court Lets Nvidia's Crypto Lawsuit Move Forward",
        "Trump's World Liberty Acquires ETH, LINK, and AAVE in $12M Crypto Shopping Spree",
    ]

    for example in examples:
        print(f'Example: {example}')
        response = llm.get_signal(example)
        print(response)

    """
    Example: Bitcoin ETF ads spotted on China’s Alipay payment app
    {
        'btc_signal': 1,
        'eth_signal': 0,
        'reasoning': "The appearance of Bitcoin ETF ads on China's Alipay, one of the
        country's largest payment platforms, is significantly bullish for Bitcoin. This
        suggests potential opening of the Chinese market to Bitcoin investment products,
        which could drive substantial new demand given China's large investor base.
        This is particularly notable given China's previous strict stance against cryptocurrencies.
        For Ethereum, while crypto news can have ecosystem-wide effects, this news specifically
        concerns Bitcoin ETFs and doesn't directly impact Ethereum's fundamentals or market
        position, hence a neutral signal."
    }

    Example: U.S. Supreme Court Lets Nvidia’s Crypto Lawsuit Move Forward
    {
        'btc_signal': 0,
        'eth_signal': 0,
        'reasoning': "The Supreme Court's decision to allow a lawsuit against Nvidia to
        proceed is primarily a corporate legal matter affecting Nvidia rather than
        cryptocurrencies directly. The lawsuit concerns historical revenue reporting
        practices and doesn't impact current cryptocurrency operations, mining capabilities,
        or market fundamentals. While the news is crypto-related, it's unlikely to cause
        any significant price movement in either BTC or ETH as it doesn't affect their
        current utility, adoption, or regulatory status."
    }

    {
        'btc_signal': 0,
        'eth_signal': 1,
        'reasoning': "Trump's World Liberty has made a $12M cryptocurrency purchase
        focusing on ETH and ETH-ecosystem tokens (LINK, AAVE). This is directly positive
        for ETH as it represents significant institutional buying pressure and strengthens
        the Ethereum ecosystem. While large crypto purchases generally create positive market
        sentiment, this news is specifically focused on ETH and its ecosystem,
        making it neutral for BTC as attention might actually be drawn away from Bitcoin
        to Ethereum in the short term."
    }
    """
