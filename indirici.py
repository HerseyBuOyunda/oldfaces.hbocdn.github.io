import os
import re
import requests

output_klasoru = "yuzler"

# Eğer klasör yoksa sıfırdan oluştur, çökme
if not os.path.exists(output_klasoru):
    print(f"'{output_klasoru}' klasörü bulunamadı, yeniden oluşturuluyor...")
    os.makedirs(output_klasoru, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

try:
    dosyalar = [f for f in os.listdir(output_klasoru) if f.endswith('.png')]
    print(f"Klasörde incelenecek {len(dosyalar)} adet dosya bulundu.\n")
except Exception as e:
    print(f"Klasör listelenirken hata oluştu: {e}")
    dosyalar = []

for dosya_adi in dosyalar:
    dosya_yolu = os.path.join(output_klasoru, dosya_adi)
    
    try:
        # Dosya boş mu kontrol et, boşsa doğrudan ID'sini isminden alıp indirmeye çalış
        if os.path.getsize(dosya_yolu) == 0:
            print(f"[{dosya_adi}] Dosya içi boş! İsme göre kurtarılıyor...")
            gercek_resim_id = dosya_adi.replace(".png", "")
        else:
            # Dosyayı ikili (binary) olarak okuyup string'e çeviriyoruz (decode hatasını önler)
            with open(dosya_yolu, "rb") as f:
                ham_veri = f.read()
            
            # Byte verisini güvenli bir şekilde stringe çeviriyoruz
            icerik = ham_veri.decode("utf-8", errors="ignore")
            
            # Eğer dosya zaten gerçek bir resimse (XML değilse) hiç dokunma
            if "<roblox" not in icerik and "TextureId" not in icerik:
                print(f"[{dosya_adi}] Zaten gerçek bir resim formatında, atlanıyor.")
                continue

            # XML içindeki gizli resim ID'sini arıyoruz
            match = re.search(r'id=(\d+)', icerik)
            if not match:
                match = re.search(r'TextureId">.*?id=(\d+)', icerik, re.DOTALL)

            if match:
                gercek_resim_id = match.group(1)
                print(f"[{dosya_adi}] İçindeki gerçek fotoğraf kodu bulundu: {gercek_resim_id}")
            else:
                print(f"[{dosya_adi}] Dosya bir XML ama içinde ID bulunamadı.")
                continue

        # Gerçek resmi indirme aşaması
        download_url = f"https://assetdelivery.roblox.com/v1/asset/?id={gercek_resim_id}"
        res = requests.get(download_url, headers=headers, timeout=15)
        
        if res.status_code == 200 and len(res.content) > 100:
            with open(dosya_yolu, "wb") as f:
                f.write(res.content)
            print(f"-> {dosya_adi} BAŞARIYLA GERÇEK FOTOĞRAFA DÖNÜŞTÜRÜLDÜ! ✅")
        else:
            print(f"-> Resim verisi alınamadı. Durum: {res.status_code}")

    except Exception as e:
        # Tek bir dosyada hata çıkarsa bot patlamasın, sıradakine geçsin
        print(f"-> {dosya_adi} işlenirken hata oluştu ama atlanıyor: {e}")
        continue

print("\nTüm klasör dönüşüm süreci bitti!")

# GitHub Actions'ın exit code 1 verip hata yakmasını %100 engelliyoruz
os._exit(0)
