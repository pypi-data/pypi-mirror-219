from engine import TradingEngine
from config import parseConfig

def main()->None:
    config=parseConfig()
    engine=TradingEngine(**config)
    engine.start()

if __name__=='__main__':
    main()