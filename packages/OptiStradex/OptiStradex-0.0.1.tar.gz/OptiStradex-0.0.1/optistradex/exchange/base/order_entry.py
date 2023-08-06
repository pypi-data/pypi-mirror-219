from abc import ABCMeta
from typing import List
from optistradex.kernel import Order, Position

class _OrderEntry(metaclass=ABCMeta):
    

    async def accounts(self) -> List[Position]: 
        return []

    async def balance(self) -> List[Position]:
        return []

    async def newOrder(self, order: Order) -> bool:
       
        raise NotImplementedError()

    async def cancelOrder(self, order: Order) -> bool:

        raise NotImplementedError()