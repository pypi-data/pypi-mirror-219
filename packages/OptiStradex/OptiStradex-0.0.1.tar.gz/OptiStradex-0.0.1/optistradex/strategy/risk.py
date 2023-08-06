from typing import Optional, TYPE_CHECKING

from kernel import Position

if TYPE_CHECKING:
    from ..engine import StrategyManager


class RiskModule():
    _manager: "StrategyManager"

    def risk(self, position: Optional[Position] = None) -> str:  # TODO
        
        return self._manager.risk(position=position)