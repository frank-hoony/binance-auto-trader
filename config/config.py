# 환경변수로 설정하거나 이 파일에 직접 입력
TELEGRAM_CONFIG = {
    'api_id': '20110521',  # 여기에 실제 API ID 입력
    'api_hash': '1f370bb5016a19cc08141cb982c2a5b1',  # 여기에 실제 API Hash 입력
    'session_name': 'gateio_trader',
    'phone_number': '+821041139222'  # 첫 로그인시 필요
}


# 트레이딩 신호 키워드 설정
TRADING_KEYWORDS = [
    'BUY', 'SELL', 'LONG', 'SHORT',
    '매수', '매도', '롱', '숏',
    'ENTRY', 'TARGET', 'STOP',
    'TP', 'SL', 'USDT', 'BTC', 'ETH'
]
