import os
import requests

output_klasoru = "yuzler"
os.makedirs(output_klasoru, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Roblox Kataloğundaki tüm yüzler taranıyor...")

# 1. ADIM: Roblox API'sinden "Face" (Yüz) kategorisindeki eşyaların ID'lerini topluyoruz
# Eşya türü (AssetType) 2 olanlar Roblox'ta doğrudan 'Face' (Yüz) dokularını temsil eder.
search_url = "https://catalog.roblox.com/v1/search/items/details?Category=11&Subcategory=5&AssetTypes=2&Limit=30"

yuz_id_listesi = []

try:
    response = requests.get(search_url, headers=headers, timeout=15)
    if response.status_code == 200:
        data = response.json()
        # API'den dönen tüm eşyaların ID'lerini ayıklıyoruz
        for item in data.get("data", []):
            if "id" in item:
                yuz_id_listesi.append(item["id"])
        print(f"Toplam {len(yuz_id_listesi)} adet klasik yüz ID'si başarıyla toplandı!")
    else:
        print(f"Roblox Kataloğuna bağlanılamadı. Durum Kodu: {response.status_code}")
except Exception as e:
    print(f"ID'ler toplanırken hata oluştu: {e}")

# 2. ADIM: Toplanan tüm ID'leri sırayla indiriyoruz
for asset_id in yuz_id_listesi:
    # GitHub sunucuları engellenmediği için doğrudan Roblox assetdelivery API'sini kullanıyoruz
    url = f"https://assetdelivery.roblox.com/v1/asset/?id={asset_id}"
    print(f"ID {asset_id} Roblox sunucularından çekiliyor...")
    
    try:
        res = requests.get(url, headers=headers, stream=True, timeout=15)
        if res.status_code == 200:
            dosya_yolu = os.path.join(output_klasoru, f"{asset_id}.png")
            with open(dosya_yolu, "wb") as f:
                f.write(res.content)
            print(f"-> ID {asset_id} başarıyla 'yuzler' klasörüne eklendi. ✅")
        else:
            print(f"-> Hata: {asset_id} indirilemedi. Durum Kodu: {res.status_code}")
    except Exception as e:
        print(f"-> Hata oluştu: {e}")

print("\nTüm yüzlerin indirme işlemi başarıyla bitti!")
