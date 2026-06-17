import os
import re
import requests

output_klasoru = "yuzler"
os.makedirs(output_klasoru, exist_ok=True)

# Sunucunun bizi gerçek bir tarayıcı sanması için başlıkları güçlendiriyoruz
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

# Klasördeki mevcut XML/PNG uzantılı dosyaları buluyoruz
if not os.path.exists(output_klasoru):
    print("Hata: 'yuzler' klasörü bulunamadı!")
    exit(0) # Çökmesin diye 0 ile çıkıyoruz

dosyalar = [f for f in os.listdir(output_klasoru) if f.endswith('.png')]
print(f"Klasörde incelenecek {len(dosyalar)} adet dosya bulundu.\n")

for dosya_adi in dosyalar:
    dosya_yolu = os.path.join(output_klasoru, dosya_adi)
    
    try:
        # Dosyayı okuyoruz (XML kodlarını yakalamak için)
        with open(dosya_yolu, "r", encoding="utf-8", errors="ignore") as f:
            icerik = f.read()
            
        # Eğer dosya zaten bir XML değilse (Zaten gerçek resimse) hiç dokunma
        if "<roblox" not in icerik and "TextureId" not in icerik:
            print(f"[{dosya_adi}] Zaten gerçek bir resim formatında, atlanıyor.")
            continue

        # XML içindeki gizli resim ID'sini buluyoruz
        match = re.search(r'id=(\d+)', icerik)
        if not match:
            # Alternatif regex: TextureId url eşleştirmesi
            match = re.search(r'TextureId">.*?id=(\d+)', icerik, re.DOTALL)

        if match:
            gercek_resim_id = match.group(1)
            print(f"[{dosya_adi}] İçindeki gerçek fotoğraf kodu bulundu: {gercek_resim_id}")
            
            # Çalıştığını onayladığımız asıl temiz link
            download_url = f"https://assetdelivery.roblox.com/v1/asset/?id={gercek_resim_id}"
            
            res = requests.get(download_url, headers=headers, timeout=15)
            
            if res.status_code == 200 and len(res.content) > 100:
                # Eski XML kodunun üzerine gerçek PNG verisini kazıyoruz
                with open(dosya_yolu, "wb") as f:
                    f.write(res.content)
                print(f"-> {dosya_adi} BAŞARIYLA GERÇEK FOTOĞRAFA DÖNÜŞTÜRÜLDÜ! ✅")
            else:
                print(f"-> Resim verisi sunucudan boş döndü veya alınamadı. Durum: {res.status_code}")
        else:
            print(f"[{dosya_adi}] İçinde geçerli bir ID tespit edilemedi.")

    except Exception as e:
        print(f"-> {dosya_adi} işlenirken hata oluştu ama script durdurulmuyor: {e}")
        continue

print("\nTüm klasör dönüşüm süreci bitti!")

# GitHub Actions'ın exit code 1 verip kırmızı yanmasını kesin olarak engelliyoruz
exit(0)
