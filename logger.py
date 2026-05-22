import os
import glob
from datetime import datetime

CURRENT_PROFILE = "default"

def update_legacy_logs():
    files = glob.glob("*_islem_gecmisi.md")
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        changed = False
        new_lines = []
        for line in lines:
            if line.startswith("| Tarih |") and "K/Z" not in line:
                line = "| Tarih | İşlem Tipi | Hisse | Lot | İşlem Fiyatı (TL) | Tutar (TL) | K/Z (TL) | K/Z (%) | Kalan Bütçe (TL) |\n"
                changed = True
                new_lines.append(line)
            elif changed and line.startswith("|---|"):
                new_lines.append("|---|---|---|---|---|---|---|---|---|\n")
            elif changed and line.startswith("|") and len(line.split("|")) == 9:
                parts = line.split("|")
                # Araya 2 yeni K/Z kolonu ekle
                tarih = parts[1]
                tipi = parts[2]
                hisse = parts[3]
                lot = parts[4]
                fiyat = parts[5]
                tutar = parts[6]
                butce = parts[7]
                new_line = f"|{tarih}|{tipi}|{hisse}|{lot}|{fiyat}|{tutar}| - | - |{butce}"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
                
        if changed:
            with open(file, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

def set_logger_profile(name):
    global CURRENT_PROFILE
    CURRENT_PROFILE = name
    update_legacy_logs()

def get_log_file():
    return f"{CURRENT_PROFILE}_islem_gecmisi.md"

def log_transaction(islem_tipi, hisse_kodu="-", lot="-", fiyat="-", islem_tutari="-", kalan_butce="-", kar_zarar_tl="-", kar_zarar_yuzde="-"):
    log_file = get_log_file()
    file_exists = os.path.exists(log_file)
    
    with open(log_file, "a", encoding="utf-8") as f:
        if not file_exists:
            # Dosya ilk kez oluşturuluyorsa başlıkları yazalım
            f.write(f"# {CURRENT_PROFILE.capitalize()} Portföyü - İşlem Geçmişi\n\n")
            f.write("| Tarih | İşlem Tipi | Hisse | Lot | İşlem Fiyatı (TL) | Tutar (TL) | K/Z (TL) | K/Z (%) | Kalan Bütçe (TL) |\n")
            f.write("|---|---|---|---|---|---|---|---|---|\n")
            
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Sayısal değerleri string formatına çevirme
        fiyat_str = f"{fiyat:.2f}" if isinstance(fiyat, (int, float)) else str(fiyat)
        tutar_str = f"{islem_tutari:.2f}" if isinstance(islem_tutari, (int, float)) else str(islem_tutari)
        butce_str = f"{kalan_butce:.2f}" if isinstance(kalan_butce, (int, float)) else str(kalan_butce)
        
        kz_tl_str = f"{kar_zarar_tl:+.2f}" if isinstance(kar_zarar_tl, (int, float)) else str(kar_zarar_tl)
        kz_yuzde_str = f"%{kar_zarar_yuzde:+.2f}" if isinstance(kar_zarar_yuzde, (int, float)) else str(kar_zarar_yuzde)
        
        # Tabloya yeni satırı ekle
        f.write(f"| {tarih} | {islem_tipi} | {hisse_kodu} | {lot} | {fiyat_str} | {tutar_str} | {kz_tl_str} | {kz_yuzde_str} | {butce_str} |\n")
