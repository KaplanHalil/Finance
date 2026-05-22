import os
from datetime import datetime

CURRENT_PROFILE = "default"

def set_logger_profile(name):
    global CURRENT_PROFILE
    CURRENT_PROFILE = name

def get_log_file():
    return f"{CURRENT_PROFILE}_islem_gecmisi.md"

def log_transaction(islem_tipi, hisse_kodu="-", lot="-", fiyat="-", islem_tutari="-", kalan_butce="-"):
    log_file = get_log_file()
    file_exists = os.path.exists(log_file)
    
    with open(log_file, "a", encoding="utf-8") as f:
        if not file_exists:
            # Dosya ilk kez oluşturuluyorsa başlıkları yazalım
            f.write(f"# {CURRENT_PROFILE.capitalize()} Portföyü - İşlem Geçmişi\n\n")
            f.write("| Tarih | İşlem Tipi | Hisse | Lot | İşlem Fiyatı (TL) | Tutar (TL) | Kalan Bütçe (TL) |\n")
            f.write("|---|---|---|---|---|---|---|\n")
            
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Sayısal değerleri string formatına çevirme
        fiyat_str = f"{fiyat:.2f}" if isinstance(fiyat, (int, float)) else str(fiyat)
        tutar_str = f"{islem_tutari:.2f}" if isinstance(islem_tutari, (int, float)) else str(islem_tutari)
        butce_str = f"{kalan_butce:.2f}" if isinstance(kalan_butce, (int, float)) else str(kalan_butce)
        
        # Tabloya yeni satırı ekle
        f.write(f"| {tarih} | {islem_tipi} | {hisse_kodu} | {lot} | {fiyat_str} | {tutar_str} | {butce_str} |\n")
