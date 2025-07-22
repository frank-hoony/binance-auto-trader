# trader/binance_client.py

from binance.client import Client
from config.config import BINANCE_CONFIG

class BinanceClient:
    def __init__(self):
        print("API Key:", BINANCE_CONFIG['api_key'])
        print("API Secret:", BINANCE_CONFIG['api_secret'])

        self.client = Client(
            api_key=BINANCE_CONFIG['api_key'],
            api_secret=BINANCE_CONFIG['api_secret']
        )
        # 옵션: 테스트넷 연결하려면 아래 주석 참고
        # self.client.API_URL = 'https://testnet.binance.vision/api'

    def get_account_info(self):
        return self.client.get_account()

    def get_balance(self, asset: str):
        balances = self.client.get_account()['balances']
        for b in balances:
            if b['asset'] == asset:
                return float(b['free'])
        return 0.0

    def get_current_price(self, symbol: str):
        ticker = self.client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])

