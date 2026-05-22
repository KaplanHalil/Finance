import yfinance as yf
import pandas as pd

# Örnek BIST30 hisseleri
BIST_STOCKS = [
    "AKBNK.IS", "ARCLK.IS", "ASELS.IS", "BIMAS.IS", "EKGYO.IS",
    "EREGL.IS", "FROTO.IS", "GARAN.IS", "GUBRF.IS", "HEKTS.IS",
    "ISCTR.IS", "KCHOL.IS", "KOZAA.IS", "KOZAL.IS", "KRDMD.IS",
    "PETKM.IS", "PGSUS.IS", "SAHOL.IS", "SASA.IS", "SISE.IS",
    "TAVHL.IS", "TCELL.IS", "THYAO.IS", "TKFEN.IS", "TTKOM.IS",
    "TUPRS.IS", "VAKBN.IS", "YKBNK.IS"
]

def fetch_data(stock_list=BIST_STOCKS, period="3mo"):
    data = {}
    for ticker in stock_list:
        try:
            # Sadece geçmiş veriyi çek, log veya progress bar gösterme
            hist = yf.download(ticker, period=period, progress=False)
            if not hist.empty:
                data[ticker] = hist
        except Exception as e:
            # Hata veren hisseleri atla
            pass
    return data
