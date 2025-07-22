import asyncio
from telegram_reader.chat_list_viewer import ChatListViewer
from trader.binance_client import BinanceClient


"""
telegram
async def main():
    viewer = ChatListViewer()
    await viewer.start()
    await viewer.interactive_selection()
    await viewer.stop()

if __name__ == "__main__":
    asyncio.run(main())
"""


def main():
    binance = BinanceClient()
    account_info = binance.get_account_info()
    print("계좌 정보 일부:", account_info['balances'][:5])  # 잔액 상위 5개 출력

    btc_balance = binance.get_balance("BTC")
    print(f"보유 BTC: {btc_balance}")

    price = binance.get_current_price("BTCUSDT")
    print(f"현재 BTC 가격: {price} USD")

if __name__ == "__main__":
    main()

