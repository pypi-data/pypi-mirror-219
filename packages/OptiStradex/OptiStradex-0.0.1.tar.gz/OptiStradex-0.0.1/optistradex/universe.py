import os
import itertools
import functools
import pandas as pd
from typing import Callable, List

class OptiStradexException(Exception):
    pass


@functools.lru_cache()
def _in_cpp() -> bool:
    _cpp = os.environ.get("OPTISTRADERX_USE_CPP", "").lower() in ("1", "on")

    try:
        from optistradex.binding import (  
            SideCpp,
            EventTypeCpp,
            DataTypeCpp,
            InstrumentTypeCpp,
            OrderTypeCpp,
            OrderFlagCpp,
            OrderBookCpp,
            ExchangeTypeCpp,
            InstrumentCpp,
            DataCpp,
            EventCpp,
            OrderCpp,
            TradeCpp,
        )
    except ImportError:
        if _cpp:
            
            raise
        return False

    return _cpp


def id_generator() -> Callable[[], int]:
    __c = itertools.count()

    def _gen_id() -> int:
        return next(__c)

    return _gen_id


def _merge(lst1: List, lst2: List, sum: bool = True) -> List:
   
    df1 = pd.DataFrame(lst1, columns=("val1", "date1"))
    df1.set_index("date1", inplace=True)
    

    df2 = pd.DataFrame(lst2, columns=("val2", "date2"))
    df2.set_index("date2", inplace=True)
    

    df = df1.join(df2, how="outer")

    
    df.fillna(method="ffill", inplace=True)
    df.fillna(0.0, inplace=True)

    if sum:
        df = df.sum(axis=1)
    else:
        df = df.mean(axis=1)

    df = df.reset_index().values.tolist()

    return [(b, a.to_pydatetime()) for a, b in df]