from enum import Enum
from typing import List

class BaseEnum(Enum):
    def __str__(self) -> str:
        return f"{self.value}"
    
    @classmethod
    def members(cls) -> List[str]:
        return list(cls.__members__.keys())

class TradingType(BaseEnum):
    LIVE="LIVE"
    SIMULATION="SIMULATION"
    BACKTEST="BACKTEST"

class EventType(BaseEnum):
    
    ERROR = "ERROR"
    START = "START"
    EXIT = "EXIT"
    
    BOUGHT = "BOUGHT"
    SOLD = "SOLD"
    RECEIVED = "RECEIVED"
    REJECTED = "REJECTED"
    CANCELED = "CANCELED"

    
    HEARTBEAT = "HEARTBEAT"

    
    TRADE = "TRADE"

    
    OPEN = "OPEN"
    CANCEL = "CANCEL"
    CHANGE = "CHANGE"
    FILL = "FILL"

    
    DATA = "DATA"

    
    HALT = "HALT"
    CONTINUE = "CONTINUE"

class DataType(BaseEnum):
    DATA = "DATA"
    ERROR = "ERROR"

    ORDER = "ORDER"
    TRADE = "TRADE"

class Side(BaseEnum):
    BUY="BUY"
    SELL="SELL"

class InstrumentType(BaseEnum):
    EQUITY="EQUITY"
    BOND="BOND"
    COMMODITY="COMMODITY"
    FUTURE="FUTURE"
    OPTION="OPTION"
    INDEX="INDEX"
    OTHER="OTHER"

class OrderType(BaseEnum):
    LIMIT="LIMIT"
    MARKET="MARKET"
    STOP="STOP"

class OrderValidityType(BaseEnum):
    NONE="NONE"
    FILL_OR_KILL="FILL_OR_KILL"
    ALL_OR_NONE="ALL_OR_NONE"
    IMMEDIATE_OR_CANCEL="IMMEDIATE_OR_CANCEL"


class OptionType(BaseEnum):
    CALL="CALL"
    PUT="PUT"

class ExitRoutine(BaseEnum):
    NONE = "NONE"
    CLOSE_ALL = "CLOSE_ALL"

