import os
import json
import requests

# JSON dosyasını açıp içindeki tüm ID'leri otomatik listeye yüklüyoruz
try:
    with open("oldface.json", "r", encoding="utf-8") as f:
        yuz_id_listesi = json.load(f)
except Exception as e:
    print(f"oldface.json dosyası okunamadı: {e}")
    yuz_id_listesi = []

output_klasoru = "yuzler"
os.makedirs(output_klasoru, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for asset_id in yuz_id_listesi:
    url = f"https://assetdelivery.roblox.com/v1/asset/?id={asset_id}"
    print(f"ID {asset_id} Roblox'tan indiriliyor...")
    
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        if response.status_code == 200:
            dosya_yolu = os.path.join(output_klasoru, f"{asset_id}.png")
            with open(dosya_yolu, "wb") as f:
                f.write(response.content)
            print(f"-> ID {asset_id} başarıyla indirildi.")
        else:
            print(f"-> Hata: {asset_id} indirilemedi. Durum Kodu: {response.status_code}")
    except Exception as e:
        print(f"-> Hata oluştu: {e}")

print("Tüm yüzlerin indirme işlemi bitti.")
