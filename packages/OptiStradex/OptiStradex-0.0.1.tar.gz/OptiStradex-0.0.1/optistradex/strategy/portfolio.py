from typing import Union,List,Optional,TYPE_CHECKING
from kernel import Instrument,Position,ExchangeType
import pandas as pd

class PortfolioModule():
    _manager:'StrategyManager'

    def positions(self):
        pass

    def portfolio(self):
        pass

    def priceHistory(self,instrument:Optional[Instrument]=None)->Union[dict,pd.Dataframe]:
        return self._manager.priceHistory(instrument=instrument)