import yfinance as yf
import pandas as pd
import sys
import os

# Örnek BIST30 hisseleri
BIST_STOCKS = [
    "AKBNK.IS", "ARCLK.IS", "ASELS.IS", "BIMAS.IS", "EKGYO.IS",
    "EREGL.IS", "FROTO.IS", "GARAN.IS", "GUBRF.IS", "HEKTS.IS",
    "ISCTR.IS", "KCHOL.IS", "KOZAA.IS", "KOZAL.IS", "KRDMD.IS",
    "PETKM.IS", "PGSUS.IS", "SAHOL.IS", "SASA.IS", "SISE.IS",
    "TAVHL.IS", "TCELL.IS", "THYAO.IS", "TKFEN.IS", "TTKOM.IS",
    "TUPRS.IS", "VAKBN.IS", "YKBNK.IS"
]

def fetch_data(stock_list=None, period="3mo"):
    if stock_list is None:
        stock_list = BIST_STOCKS
    data = {}
    
    # yfinance kütüphanesinin ekrana basabileceği 
    # "Failed download" veya "possibly delisted" gibi hataları gizle
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        try:
            sys.stdout = devnull
            sys.stderr = devnull
            
            for ticker in stock_list:
                try:
                    hist = yf.download(ticker, period=period, progress=False)
                    if not hist.empty:
                        data[ticker] = hist
                except Exception:
                    pass
        finally:
            # İşlem bitince çıktıları eski haline getir
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
    return data
