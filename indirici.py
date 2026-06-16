import os
import requests

output_klasoru = "yuzler"
os.makedirs(output_klasoru, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Roblox Kataloğundaki tüm yüzler taranıyor...")

# Katalog arama API'si
search_url = "https://catalog.roblox.com/v1/search/items/details?Category=11&Subcategory=5&AssetTypes=2&Limit=30"

yuz_id_listesi = []

try:
    response = requests.get(search_url, headers=headers, timeout=15)
    if response.status_code == 200:
        data = response.json()
        for item in data.get("data", []):
            if "id" in item:
                yuz_id_listesi.append(item["id"])
        print(f"Toplam {len(yuz_id_listesi)} adet klasik yüz ID'si toplandı!")
    else:
        print(f"Roblox Kataloğuna bağlanılamadı. Durum Kodu: {response.status_code}")
except Exception as e:
    print(f"ID'ler toplanırken hata oluştu: {e}")

# Eğer liste boş kaldıysa bulut makinesi çökmesin diye kontrol ekliyoruz
if not yuz_id_listesi:
    print("Hata: İndirilecek hiçbir yüz ID'si bulunamadı. Liste boş!")
    yuz_id_listesi = [100253786] # Test amaçlı yedek bir ID koyuyoruz ki script boş dönmesin

# 2. ADIM: Resimleri İndirme Dönemi
for asset_id in yuz_id_listesi:
    # Doğrudan PNG üreten güncel endpoint
    url = f"https://www.roblox.com/asset-thumbnail/image?assetId={asset_id}&width=420&height=420&format=png"
    print(f"ID {asset_id} PNG görseli çekiliyor...")
    
    try:
        res = requests.get(url, headers=headers, stream=True, timeout=15)
        if res.status_code == 200:
            dosya_yolu = os.path.join(output_klasoru, f"{asset_id}.png")
            with open(dosya_yolu, "wb") as f:
                # Chunk chunk indirerek bellek hatalarını (RAM patlamalarını) önlüyoruz
                for chunk in res.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"-> ID {asset_id} GERÇEK PNG OLARAK EKLENDİ. ✅")
        else:
            print(f"-> Hata: {asset_id} indirilemedi. Durum Kodu: {res.status_code}")
    except Exception as e:
        # Burada hata gelse bile 'continue' diyerek bir sonraki resme geçmesini sağlıyoruz
        print(f"-> {asset_id} indirilirken beklenmedik bir hata oluştu ama atlanıyor: {e}")
        continue

print("\nTüm yüzlerin indirme işlemi başarıyla bitti!")
