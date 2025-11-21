import hashlib
import numpy as np
from PIL import Image
from pathlib import Path




IMG_PATH = "OrijinalResim.jpg"


img = Image.open(IMG_PATH).convert("RGB")
arr = np.array(img)

original_hash = hashlib.sha256(arr.tobytes()).hexdigest()


Path("orijinal_hash.txt").write_text(original_hash)
print("✅ Orijinal hash kaydedildi.")


stored_hash = Path("orijinal_hash.txt").read_text().strip()

new_hash = hashlib.sha256(np.array(Image.open(IMG_PATH).convert("RGB")).tobytes()).hexdigest()

if stored_hash == new_hash:
    print("✅ Görüntü doğrulandı (değişiklik yok).")
else:
    print("❌ Görüntü değişmiş")

arr[0, 0, 0] = (int(arr[0, 0, 0]) + 1) % 256
Image.fromarray(arr).save("degistirilmis.png")
print("🖼️ Görüntü değiştirildi ve degistirilmis.png olarak kaydedildi.")


mod_hash = hashlib.sha256(np.array(Image.open("degistirilmis.png").convert("RGB")).tobytes()).hexdigest()

# 9. Değiştirilen görüntüyle doğrulama
if stored_hash == mod_hash:
    print("✅ Aynı hash (değişiklik yok).")
else:
    print("❌ Farklı hash! Görüntü değiştirilmiş.")