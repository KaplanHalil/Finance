import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator

def analyze_stocks(data_dict):
    recommendations = []
    
    for ticker, df in data_dict.items():
        if len(df) < 50: # En az 50 günlük veri olmalı
            continue
            
        # "Close" sütununu alıp düzleştiriyoruz (bazı sürümlerde yfinance MultiIndex dönebilir)
        close_prices = df['Close'].squeeze()
        if isinstance(close_prices, pd.DataFrame):
             close_prices = close_prices.iloc[:, 0]
             
        # Teknik Göstergelerin Hesaplanması
        rsi = RSIIndicator(close=close_prices, window=14).rsi()
        macd = MACD(close=close_prices).macd_diff()
        sma50 = SMAIndicator(close=close_prices, window=50).sma_indicator()
        sma200 = SMAIndicator(close=close_prices, window=200).sma_indicator()
        
        last_price = float(close_prices.iloc[-1])
        last_rsi = float(rsi.iloc[-1])
        last_macd_diff = float(macd.iloc[-1])
        last_sma50 = float(sma50.iloc[-1])
        
        score = 0
        reasons = []
        
        # 1. Kriter: RSI < 45 ise ucuzlamış sayılabilir
        if last_rsi < 45:
            score += 1
            reasons.append(f"RSI Düşük ({last_rsi:.2f})")
            
        # 2. Kriter: MACD pozitife döndüyse yukarı ivme başlamış olabilir
        if last_macd_diff > 0:
            score += 1
            reasons.append("MACD Al Veriyor")
            
        # 3. Kriter: Fiyat 50 günlük ortalamanın üstündeyse güçlü duruyor demektir
        if last_price > last_sma50:
            score += 1
            reasons.append("Fiyat 50 Günlük Ortalamanın Üzerinde")
            
        # Skor 2 veya daha büyükse tavsiye listesine ekle
        if score >= 2:
            recommendations.append({
                'Hisse': ticker.replace('.IS', ''),
                'Fiyat': last_price,
                'RSI': last_rsi,
                'Skor': score,
                'Nedenler': ", ".join(reasons)
            })
            
    # En yüksek skora ve ardından en düşük RSI'a göre sıralama (En potansiyelliler üstte)
    recommendations.sort(key=lambda x: (-x['Skor'], x['RSI']))
    return recommendations

def evaluate_portfolio(portfolio, data_dict):
    evaluations = []
    
    for ticker, info in portfolio.items():
        yf_ticker = f"{ticker}.IS"
        if yf_ticker not in data_dict:
            continue
            
        df = data_dict[yf_ticker]
        if len(df) < 50:
            continue
            
        close_prices = df['Close'].squeeze()
        if isinstance(close_prices, pd.DataFrame):
             close_prices = close_prices.iloc[:, 0]
             
        rsi = RSIIndicator(close=close_prices, window=14).rsi()
        macd = MACD(close=close_prices).macd_diff()
        sma50 = SMAIndicator(close=close_prices, window=50).sma_indicator()
        
        last_price = float(close_prices.iloc[-1])
        last_rsi = float(rsi.iloc[-1])
        last_macd_diff = float(macd.iloc[-1])
        last_sma50 = float(sma50.iloc[-1])
        
        action = "Tut"
        reasons = []
        
        if last_rsi > 70:
            action = "Sat"
            reasons.append(f"RSI Aşırı Alımda ({last_rsi:.2f})")
            
        if last_price < last_sma50:
            action = "Sat"
            reasons.append("Fiyat 50 Günlük Ortalamanın Altında")
            
        if last_macd_diff < 0:
            reasons.append("MACD Negatif")
            if action == "Tut" and last_macd_diff < -1:
                action = "Sat"
                
        if not reasons:
            reasons.append("Trend Olumlu")
            
        maliyet = info.get('maliyet', last_price)
        k_z = 0
        if maliyet > 0:
            k_z = ((last_price - maliyet) / maliyet) * 100
            
        evaluations.append({
            'Hisse': ticker,
            'Durum': action,
            'Fiyat': last_price,
            'Maliyet': maliyet,
            'K/Z %': k_z,
            'Lot': info['lot'],
            'Nedenler': ", ".join(reasons)
        })
        
    return evaluations
