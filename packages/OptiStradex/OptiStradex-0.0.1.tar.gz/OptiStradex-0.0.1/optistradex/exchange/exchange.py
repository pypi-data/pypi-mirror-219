from typing import List
from abc import abstractmethod
from kernel import Instrument,ExchangeType

class Exchange():
    def __init__(self,exchange:ExchangeType) -> None:
        self._exchange:ExchangeType=exchange

    def exchange(self)->ExchangeType:
        return self._exchange

    @abstractmethod
    async def connect(self)->None:
        pass

    async def lookup(self,instrument:Instrument)->List[Instrument]:
        return []
