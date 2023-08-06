from ibapi.client import EClient  
from ibapi.commission_report import CommissionReport  
from ibapi.contract import Contract  
from ibapi.execution import Execution, ExecutionFilter  
from ibapi.order import Order  
from ibapi.wrapper import EWrapper 

from optistradex.config import EventType, Side, TradingType
from optistradex.kernel import Event, ExchangeType, Instrument
from optistradex.kernel import Order as optistradexOrder
from optistradex.kernel import Position, Trade
from optistradex.exchange import Exchange

import asyncio
import threading
from datetime import datetime
from queue import Queue
from random import randint
from typing import Any, AsyncGenerator, Dict, List, Set, Tuple, Union

class _TWSAPI(EWrapper, EClient):
    def __init__(
        self,
        account: str,
        exchange: ExchangeType,
        delayed: bool,
        order_event_queue: Queue,
        market_data_queue: Queue,
        contract_info_queue: Queue,
        account_position_queue: Queue,
    ) -> None:
        EClient.__init__(self, self)
        self.nextOrderId: int = 1
        self.nextReqId = 1

       
        self._account = account

        
        self._exchange = exchange

        
        self._delayed = delayed

        self._mkt_data_map: Dict[int, Tuple[Contract, Instrument]] = {}
        self._mkt_data_map_rev: Dict[Contract, int] = {}

        self._order_event_queue = order_event_queue
        self._market_data_queue = market_data_queue
        self._contract_info_queue = contract_info_queue
        self._account_position_queue = account_position_queue

        self._positions: List[Position] = []

    def reqPositions(self) -> None:
        super().reqPositions()

    def nextValidId(self, orderId: int) -> None:
        super().nextValidId(orderId)
        self.nextOrderId = orderId

    def reqContractDetails(self, contract: Contract) -> None:
        super().reqContractDetails(self.nextReqId, contract)
        self.nextReqId += 1

    def placeOrder(self, contract: Contract, order: Order) -> str:
        order.account = self._account
        super().placeOrder(self.nextOrderId, contract, order)
        self.nextOrderId += 1
        return str(self.nextOrderId - 1)

    def cancelOrder(self, order: optistradexOrder) -> None:
        super().cancelOrder(order.id)

    def contractDetails(self, reqId: int, contractDetails: dict) -> None:
        self._contract_info_queue.put(contractDetails)

    def orderStatus(
        self,
        orderId: int,
        status: str,
        filled: float,
        remaining: float,
        avgFillPrice: float,
        permId: str,
        parentId: str,
        lastFillPrice: float,
        clientId: str,
        whyHeld: str,
        mktCapPrice: float,
    ) -> None:
        self._order_event_queue.put(
            dict(
                orderId=orderId,
                status=status,
                filled=filled,
                avgFillPrice=avgFillPrice
            )
        )

    def subscribeMarketData(self, instrument: Instrument) -> None:
        contract = _constructContract(instrument)
        self._mkt_data_map[self.nextReqId] = (contract, instrument)
        self._mkt_data_map_rev[contract] = self.nextReqId

        if self._delayed:
            self.reqMarketDataType(3)

        self.reqMktData(self.nextReqId, contract, "", False, False, [])
        self.nextReqId += 1

    def cancelMarketData(self, contract: Contract) -> None:
        id = self._mkt_data_map_rev[contract]
        self.cancelMktData(id)
        del self._mkt_data_map_rev[contract]
        del self._mkt_data_map[id]

    def reqExecutions(self) -> None:
        super().reqExecutions(self.nextReqId, ExecutionFilter())
        self.nextReqId += 1

    def execDetails(self, reqId: int, contract: Contract, execution: Execution) -> None:
        super().execDetails(reqId, contract, execution)
        self._order_event_queue.put(
            dict(
                orderId=execution.orderId,
                status="Execution",
                filled=execution.cumQty,
                
                avgFillPrice=execution.avgPrice,  # TODO execution.price?
                
            )
        )

    def commissionReport(self, commissionReport: CommissionReport) -> None:
        super().commissionReport(commissionReport)


    def execDetailsEnd(self, reqId: int) -> None:
        super().execDetailsEnd(reqId)
        

    def error(self, reqId: int, errorCode: int, errorString: str) -> None:
        if errorCode in (
            110,  
            201, 
        ):
            self._order_event_queue.put(
                dict(
                    orderId=reqId,
                    status="Rejected",
                )
            )
        elif errorCode in (
            136,  
            161,  
            10148,  
        ):
            self._order_event_queue.put(
                dict(
                    orderId=reqId,
                    status="RejectedCancel",
                )
            )
        elif errorCode in (202,): 
            ...
            
        else:
            super().error(reqId, errorCode, errorString)

    def tickPrice(self, reqId: int, tickType: int, price: float, attrib: str) -> None:
        

        if self._delayed:
            tick_type = 68  
        else:
            tick_type = 4  

        if tickType == tick_type:
            self._market_data_queue.put(
                dict(
                    contract=self._mkt_data_map[reqId][0],
                    instrument=self._mkt_data_map[reqId][1],
                    price=price,
                )
            )

    def position(
        self, account: str, contract: Contract, position: float, avgCost: float
    ) -> None:
        super().position(account, contract, position, avgCost)
        self._positions.append(
            Position(
                size=position,
                price=avgCost / position,
                timestamp=datetime.now(),
                instrument=_constructInstrument(contract),
                exchange=self._exchange,
                trades=[],
            )
        )

    def accountSummaryEnd(self, reqId: int) -> None:
        self._account_position_queue.put(self._positions)
        self._positions = []


class InteractiveBrokersExchange(Exchange):

    def __init__(
        self,
        trading_type: TradingType,
        verbose: bool,
        account: str = "",
        delayed: bool = True,
        **kwargs: dict
    ) -> None:
        self._trading_type = trading_type
        self._verbose = verbose

        if self._trading_type == TradingType.LIVE:
            super().__init__(ExchangeType("interactivebrokers"))
        else:
            super().__init__(ExchangeType("interactivebrokerspaper"))

        self._orders: Dict[str, Order] = {}

        
        self._order_received_map_set: Dict[str, asyncio.Event] = {}
        self._order_received_map_get: Dict[str, asyncio.Event] = {}
        self._order_received_res: Dict[str, bool] = {}

        
        self._order_cancelled_map_set: Dict[str, asyncio.Event] = {}
        self._order_cancelled_map_get: Dict[str, asyncio.Event] = {}
        self._order_cancelled_res: Dict[str, bool] = {}

        
        self._finished_orders: Set[str] = set()

       
        self._order_event_queue: Queue[Dict[str, Union[str, int, float]]] = Queue()
        self._market_data_queue: Queue[
            Dict[str, Union[str, int, float, Instrument]]
        ] = Queue()
        self._contract_lookup_queue: Queue[Contract] = Queue()
        self._account_position_queue: Queue[Position] = Queue()
        self._api = _TWSAPI(
            account,
            self.exchange(),
            delayed,
            self._order_event_queue,
            self._market_data_queue,
            self._contract_lookup_queue,
            self._account_position_queue,
        )

    async def instruments(self) -> List[Instrument]:
        
        return []

    async def connect(self) -> None:
       
        if self._trading_type == TradingType.LIVE:
            print("*" * 100)
            print("*" * 100)
            print("WARNING: LIVE TRADING")
            print("*" * 100)
            print("*" * 100)
            self._api.connect("127.0.0.1", 7496, randint(0, 10000))
            self._api_thread = threading.Thread(target=self._api.run, daemon=True)
            self._api_thread.start()

        else:
            self._api.connect("127.0.0.1", 7497, randint(0, 10000))
            self._api_thread = threading.Thread(target=self._api.run, daemon=True)
            self._api_thread.start()

        while self._api.nextOrderId is None:
            print("waiting for IB connect...")
            await asyncio.sleep(1)

        print("IB connected!")

    async def lookup(self, instrument: Instrument) -> List[Instrument]:
        self._api.reqContractDetails(_constructContract(instrument))
        i = 0
        while i < 5:
            if self._contract_lookup_queue.qsize() > 0:
                ret = []
                while self._contract_lookup_queue.qsize() > 0:
                    contract_details = self._contract_lookup_queue.get()
                    ret.append(_constructInstrument(contract_details.contract))
                return ret
            else:
                await asyncio.sleep(1)
                i += 1
        return []


    async def subscribe(self, instrument: Instrument) -> None:
        self._api.subscribeMarketData(instrument)

    def _create_order_received(self, orderId: str) -> None:
        
        self._order_received_map_get[orderId] = asyncio.Event()
        self._order_received_map_set[orderId] = asyncio.Event()

    async def _send_order_received(
        self, orderId: str, ret: bool, waitfor: bool = True
    ) -> None:
        
        self._order_received_res[orderId] = ret

        
        if orderId in self._order_received_map_set:
            self._order_received_map_set[orderId].set()

            await asyncio.sleep(0)

            await self._order_received_map_get[orderId].wait()

    async def _send_cancel_received(
        self, orderId: str, ret: bool, waitfor: bool = True
    ) -> None:
        
        self._order_cancelled_res[orderId] = ret

        if orderId in self._order_cancelled_map_set:
            self._order_cancelled_map_set[orderId].set()

            
            await asyncio.sleep(0)

            
            await self._order_cancelled_map_get[orderId].wait()

    async def _consume_order_received(self, orderId: str) -> bool:
       
        if orderId in self._order_received_res:
            return self._order_received_res.pop(orderId)

        
        if orderId in self._order_received_map_set:
            return False

        
        self._order_received_map_get[orderId] = asyncio.Event()
        self._order_received_map_set[orderId] = asyncio.Event()

       
        await self._order_received_map_set[orderId].wait()

        self._order_received_map_get[orderId].set()

        return self._order_received_res.pop(orderId)

    async def _consume_cancel_received(self, orderId: str) -> bool:
       
        if orderId in self._order_cancelled_res:
            return self._order_cancelled_res.pop(orderId)

        if orderId in self._order_cancelled_map_set:
            return False

        self._order_cancelled_map_get[orderId] = asyncio.Event()
        self._order_cancelled_map_set[orderId] = asyncio.Event()

        await self._order_cancelled_map_set[orderId].wait()

        self._order_cancelled_map_get[orderId].set()

        if self._order_cancelled_res[orderId]:
            self._finished_orders.add(orderId)

        return self._order_cancelled_res.pop(orderId)

    async def tick(self) -> AsyncGenerator[Any, Event]:  # type: ignore[override]
       
        while True:
            
            while self._order_event_queue.qsize() > 0:
                order_data = self._order_event_queue.get()
                status = order_data["status"]
                order = self._orders[str(order_data["orderId"])]
                if status in (
                    "ApiPending",
                    "PendingSubmit",
                    "PendingCancel",
                    "PreSubmitted",
                    "ApiCancelled",
                ):
                    continue

                elif status in ("Inactive",):
                    self._finished_orders.add(order.id)

                elif status in ("Rejected",):
                    self._finished_orders.add(order.id)
                    await self._send_order_received(order.id, False)

                elif status in ("RejectedCancel",):
                    await self._send_cancel_received(order.id, False)

                elif status in ("Submitted",):
                    await self._send_order_received(order.id, True)

                elif status in ("Cancelled",):
                    self._finished_orders.add(order.id)
                    await self._send_cancel_received(order.id, True)

                elif status in ("Filled",):

                    pass

                elif status in ("Execution",):
                    
                    order.filled = order_data["filled"]

                    
                    if order.finished():
                        self._finished_orders.add(order.id)

                        
                    t = Trade(
                        volume=order_data["filled"],  
                        price=order_data["avgFillPrice"],  
                        maker_orders=[],
                        taker_order=order,
                    )

                    t.my_order = order

                    e = Event(type=EventType.TRADE, target=t)

                   
                    await self._send_order_received(order.id, True)
                    yield e

            
            while self._market_data_queue.qsize() > 0:
                market_data = self._market_data_queue.get()
                instrument: Instrument = market_data["instrument"]  
                price: float = market_data["price"] 
                o = optistradexOrder(
                    volume=1,
                    price=price,
                    side=Side.BUY,
                    instrument=instrument,
                    exchange=self.exchange(),
                    filled=1,
                )
                t = Trade(volume=1, price=float(price), taker_order=o, maker_orders=[])
                yield Event(type=EventType.TRADE, target=t)

            await asyncio.sleep(0)
  
    async def accounts(self) -> List[Position]:  
        
        self._api.reqPositions()
        i = 0
        while i < 5:
            if self._account_position_queue.qsize() > 0:
                return [self._account_position_queue.get()]
            else:
                await asyncio.sleep(1)
                i += 1
        return []

    async def newOrder(self, order: optistradexOrder) -> bool:
    
        if order.id and order.id in self._finished_orders:
            return False


        ibcontract, iborder = _constructContractAndOrder(order)

        _temp_id = str(self._api.nextOrderId)

    
        order.id = _temp_id
        self._orders[order.id] = order

        self._api.placeOrder(ibcontract, iborder)

    
        return await self._consume_order_received(_temp_id)

    async def cancelOrder(self, order: optistradexOrder) -> bool:
        
        if not order.id:
            return False

       
        if order.id in self._finished_orders:
            return False

        
        self._api.cancelOrder(order)

        return await self._consume_cancel_received(order.id)