from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel, Field


class NewsSignal(BaseModel):
    btc_signal: Literal[1, 0, -1] = Field(
        description="""
        The impact of the news on the BTC price.
        1 if the price is expected to go up
        0 if it is expected to stay the same,
        -1 if it is expected to go down.

        If the news is not related to BTC, the signal should be 0.
        """
    )

    eth_signal: Literal[1, 0, -1] = Field(
        description="""
        The impact of the news on the ETH price.
        1 if the price is expected to go up
        0 if it is expected to stay the same,
        -1 if it is expected to go down.

        If the news is not related to ETH, the signal should be 0.
        """
    )

    reasoning: str = Field(
        description="""
        The reasoning behind the btc_signal and eth_signal extracted from the news article.
        """
    )

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the NewsSignal.
        """
        return {
            'btc_signal': self.btc_signal,
            'eth_signal': self.eth_signal,
            'reasoning': self.reasoning,
        }


class BaseNewsSignalExtractor(ABC):
    @abstractmethod
    def get_signal(
        self, text: str, output_format: Literal['dict', 'NewsSignal'] = 'dict'
    ) -> dict | NewsSignal:
        pass

    # @property
    # def model_name(self) -> str:
    #     return self.model_name
