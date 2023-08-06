import asyncio
from abc import abstractmethod
from kernel import Event,EventHandler,Order,Instrument
from config import Side
from universe import id_generator
from util import UtilsModule
from risk import RiskModule
from portfolio import PortfolioModule
from typing import Any,Optional,List

class Strategy(EventHandler, PortfolioModule, UtilsModule, RiskModule):
    _ID_GENERATOR = id_generator()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)  
        self.__inst = Strategy._ID_GENERATOR()

    def name(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return "{}-{}".format(self.__class__.__name__, self.__inst)

    @abstractmethod
    async def onTrade(self, event: Event) -> None:
        pass

    async def onOrder(self, event: Event) -> None:
        
        pass

    async def onOpen(self, event: Event) -> None:
        
        pass

    async def onCancel(self, event: Event) -> None:
        
        pass

    async def onChange(self, event: Event) -> None:
       
        pass

    async def onFill(self, event: Event) -> None:
        
        pass

    async def onData(self, event: Event) -> None:
        
        pass

    async def onHalt(self, event: Event) -> None:
        pass

    async def onContinue(self, event: Event) -> None:
        pass

    async def onError(self, event: Event) -> None:
        
        pass

    async def onStart(self, event: Event) -> None:
        
        pass

    async def onExit(self, event: Event) -> None:
        
        pass


    async def onBought(self, event: Event) -> None:
       
        pass

    async def onSold(self, event: Event) -> None:
        
        pass

    async def onTraded(self, event: Event) -> None:
        
        pass

    async def onRejected(self, event: Event) -> None:
        
        pass

    async def onCanceled(self, event: Event) -> None:
        
        pass

    
    async def newOrder(self, order: Order) -> bool:
        
        return await self._manager.newOrder(self, order)

    async def cancelOrder(self, order: Order) -> bool:
       
        return await self._manager.cancelOrder(self, order)

    async def cancel(self, order: Order) -> bool:
        
        return await self._manager.cancelOrder(self, order)

    async def buy(self, order: Order) -> bool:
        
        return await self._manager.newOrder(self, order)

    async def sell(self, order: Order) -> bool:
        
        return await self._manager.newOrder(self, order)

    async def cancelAll(self, instrument: Optional[Instrument] = None) -> List[bool]:
        
        orders = self.orders(instrument=instrument)
        if orders:
            return await asyncio.gather(*(self.cancel(order) for order in orders))
        return []

    async def closeAll(self, instrument: Optional[Instrument] = None) -> List[bool]:
       
        await self.cancelAll(instrument=instrument)

        orders = [
            Order(
                volume=p.size,
                price=0,
                side=Side.SELL if p.size > 0 else Side.BUY,
                instrument=p.instrument,
                exchange=p.exchange,
            )
            for p in self.positions(instrument=instrument)
            if p.size != 0
        ]
        return await asyncio.gather(*(self.newOrder(order) for order in orders))


