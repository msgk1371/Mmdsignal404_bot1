# Mmdsignal_bot1 - CoinEx Futures Pump Scanner
import requests, time, schedule, os
from datetime import datetime

TELEGRAM_TOKEN = "8223385896:AAEhuopBTC-nLMAEVtIKYXm4QMHK0oXjGG0"
TELEGRAM_CHAT_ID = "7174495390"

COINS = ["BTCUSDT","ETHUSDT","SOLUSDT","XRPUSDT","DOGEUSDT","ADAUSDT","AVAXUSDT","LINKUSDT","BNBUSDT","ZECUSDT","ENAUSDT","PEPEUSDT","SHIBUSDT"]

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                      data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"})
    except: pass

def get_data(s):
    try:
        t = requests.get(f"https://api.coinex.com/v1/contract/market/ticker?market={s}_PERP").json()["data"]["ticker"]
        f = requests.get(f"https://api.coinex.com/v1/contract/funding/rate?market={s}_PERP").json()["data"]
        st = requests.get(f"https://api.coinex.com/v1/contract/market/stats?market={s}_PERP").json()["data"]
        return {
            "p": float(t["last"]),
            "c": float(t["change"])*100,
            "v": float(t["vol"]),
            "fr": float(f["funding_rate"])*100,
            "ls": float(st["long_short_ratio"])
        }
    except: return None

def scan():
    signals = []
    for sym in COINS:
        d = get_data(sym)
        if not d: continue
        score = 50
        if d["c"] > 8: score += 25
        if d["fr"] < -0.01: score += 30
        if d["ls"] > 1.3: score += 20
        if d["v"] > 100_000_000: score += 15
        if score >= 90:
            signals.append(f"""
{Mmdsignal_bot1} PUMP ALERT

{sym}
قیمت: ${d["p"]:,.2f}
تغییرات ۲۴س: +{d["c"]:.2f}%
Funding: {d["fr"]:.4f}%
لانگ/شورت: {d["ls"]:.2f}
امتیاز: {score}/100
""")
    if signals:
        send("\n".join(signals))

send("@Mmdsignal_bot1 روشن شد!\nهر ۱۰ دقیقه سیگنال قوی CoinEx برات می‌فرستم")

schedule.every(10).minutes.do(scan)

if name == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
