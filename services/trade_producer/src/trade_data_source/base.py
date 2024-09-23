from abc import ABC, abstractmethod
from typing import List

# observe how I am using absolute imports here
# if you know how to use relative imports, please enlighten me :-)
from src.trade_data_source.trade import Trade

class TradeSource(ABC):

    @abstractmethod
    def get_trades(self) -> List[Trade]:
        """
        Retrieve the trades from whatever source you connect to.
        """
        pass

    @abstractmethod
    def is_done(self) -> bool:
        """
        Returns True if there are no more trades to retrieve, False otherwise.
        """
        pass