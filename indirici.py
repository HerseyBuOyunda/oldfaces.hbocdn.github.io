import os
import re
import requests

output_klasoru = "yuzler"
# Eğer klasör yoksa oluşturuyoruz
os.makedirs(output_klasoru, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 1. ADIM: Klasörde halihazırda duran XML/Kod içerikli dosyaları tarıyoruz
dosyalar = [f for f in os.listdir(output_klasoru) if f.endswith('.png')]

print(f"Klasörde incelenecek {len(dosyalar)} adet dosya bulundu.\n")

for dosya_adi in dosyalar:
    dosya_yolu = os.path.join(output_klasoru, dosya_adi)
    
    # Dosyanın içeriğini okuyoruz
    try:
        with open(dosya_yolu, "r", encoding="utf-8", errors="ignore") as f:
            icerik = f.read()
    except Exception as e:
        print(f"{dosya_adi} okunurken hata oluştu: {e}")
        continue

    # 2. ADIM: XML içindeki <Content name="TextureId"><url>...id=SAYI</url></Content> yapısını arıyoruz
    # Bu düzenli ifade (Regex) dosyadaki gerçek resim ID'sini bulup çıkarır
    match = re.search(r'name="TextureId">.*?id=(\d+)', icerik, re.DOTALL)
    
    if match:
        gercek_resim_id = match.group(1)
        print(f"[{dosya_adi}] İçindeki gerçek fotoğraf kodu bulundu: {gercek_resim_id}")
        
        # 3. ADIM: Bulunan gerçek ID ile doğrudan Roblox resim sunucusundan PNG'yi çekiyoruz
        download_url = f"https://assetdelivery.roblox.com/v1/asset/?id={gercek_resim_id}"
        
        try:
            res = requests.get(download_url, headers=headers, stream=True, timeout=15)
            if res.status_code == 200:
                # Eski XML içerikli dosyanın üzerine gerçek PNG verisini yazıyoruz
                with open(dosya_yolu, "wb") as f:
                    for chunk in res.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"-> {dosya_adi} başarıyla gerçek fotoğrafa dönüştürüldü! ✅")
            else:
                print(f"-> Resim sunucusundan indirilemedi. Durum kodu: {res.status_code}")
        except Exception as e:
            print(f"-> Resim indirilirken hata oluştu: {e}")
            
    else:
        # Eğer dosya zaten bir resimse veya içinde TextureId yoksa dokunmuyoruz
        print(f"[{dosya_adi}] İçinde yeni bir fotoğraf kodu bulunamadı veya zaten gerçek bir resim.")

print("\nTüm klasör dönüştürme işlemi başarıyla tamamlandı!")
