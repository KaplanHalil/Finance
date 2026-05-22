import sys
from budget_manager import load_budget, save_budget
from data_fetcher import fetch_data
from analyzer import analyze_stocks
from optimizer import allocate_budget

def print_separator():
    print("=" * 60)

def main():
    while True:
        budget = load_budget()
        print("\n")
        print_separator()
        print("    Borsa İstanbul Hisse Analiz ve Tavsiye Programı")
        print_separator()
        print(f"Mevcut Bütçeniz: {budget:.2f} TL")
        print("\nMenü:")
        print("1. Bütçeyi Görüntüle / Güncelle")
        print("2. Piyasayı Analiz Et ve Tavsiye Ver")
        print("3. Çıkış")
        
        choice = input("\nSeçiminiz (1/2/3): ")
        
        if choice == '1':
            try:
                new_budget_str = input(f"Yeni bütçenizi girin (TL) [Mevcut: {budget:.2f}]: ")
                if not new_budget_str.strip():
                    continue # Boş bırakılırsa iptal
                new_budget = float(new_budget_str)
                if new_budget < 0:
                    print("Bütçe negatif olamaz!")
                else:
                    save_budget(new_budget)
                    print("Bütçeniz başarıyla güncellendi.")
            except ValueError:
                print("Lütfen geçerli bir sayı girin.")
                
        elif choice == '2':
            if budget <= 0:
                print("Lütfen önce bütçenizi güncelleyin (Bütçeniz 0 TL).")
                continue
                
            print("\nPiyasa verileri çekiliyor, lütfen bekleyin... (Bu işlem birkaç saniye sürebilir)")
            data_dict = fetch_data()
            
            print("Veriler analiz ediliyor...")
            recommendations = analyze_stocks(data_dict)
            
            if not recommendations:
                print("Şu anki piyasa koşullarında stratejiye uyan hisse bulunamadı.")
                continue
                
            print("\n*** POTANSİYEL HİSSELERE AİT TEKNİK ANALİZ SONUÇLARI ***")
            for r in recommendations[:5]: # İlk 5'i göster
                print(f"- {r['Hisse']:<6}: Fiyat={r['Fiyat']:.2f} TL | Skor={r['Skor']}/3 | Neden: {r['Nedenler']}")
                
            print("\nBütçenize göre portföy oluşturuluyor...")
            portfolio, remaining = allocate_budget(budget, recommendations)
            
            if not portfolio:
                print("Bütçeniz önerilen hisselerden almak için (en az 1 lot) yetersiz.")
            else:
                print("\n" + "*" * 50)
                print("        TAVSİYE EDİLEN PORTFÖY DAĞILIMI")
                print("*" * 50)
                total_spent = 0
                for item in portfolio:
                    print(f"Hisse: {item['Hisse']:<6} | Lot: {item['Lot']:<4} | Fiyat: {item['Fiyat']:>7.2f} TL | Toplam: {item['Toplam Maliyet']:>8.2f} TL")
                    total_spent += item['Toplam Maliyet']
                    
                print("-" * 50)
                print(f"Harcanan Toplam Bütçe: {total_spent:.2f} TL")
                print(f"Kalan Nakit:          {remaining:.2f} TL")
                
        elif choice == '3':
            print("Programdan çıkılıyor. Bol kazançlar!")
            sys.exit(0)
        else:
            print("Geçersiz seçim, lütfen 1, 2 veya 3 girin.")

if __name__ == "__main__":
    main()
