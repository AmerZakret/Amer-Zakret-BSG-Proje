import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def xor_images(original_path, random_path, output_path="encrypted_image.png"):

    original = Image.open(original_path).convert("RGB")
    random_img = Image.open(random_path).convert("RGB")

    if original.size != random_img.size:
        raise ValueError(f"Görüntü boyutları eşleşmiyor: {original.size} vs {random_img.size}")

    original_array = np.array(original, dtype=np.uint8)
    random_array = np.array(random_img, dtype=np.uint8)

    # XOR işlemi
    encrypted_array = np.bitwise_xor(original_array, random_array)

    # Görüntüye çevir ve kaydet
    encrypted_image = Image.fromarray(encrypted_array)
    encrypted_image.save(output_path)

    print(f"✅ XOR şifreleme tamamlandı → {output_path}")
    return encrypted_image


xor_images("original.png", "random_image.png", "encrypted_image.png")
xor_images("encrypted_image.png", "random_image.png", "decrypted_image.png")

def compare_histograms(original_path, encrypted_path):

    original = Image.open(original_path).convert("RGB")
    encrypted = Image.open(encrypted_path).convert("RGB")

    original_array = np.array(original)
    encrypted_array = np.array(encrypted)

    plt.figure(figsize=(12, 5))

    #Orijinal
    plt.subplot(1, 2, 1)
    plt.hist(original_array.ravel(), bins=256, color='blue', alpha=0.7)
    plt.title("Orijinal Görüntü Histogramı")
    plt.xlabel("Piksel Değeri")
    plt.ylabel("Frekans")

    #Şifreli
    plt.subplot(1, 2, 2)
    plt.hist(encrypted_array.ravel(), bins=256, color='red', alpha=0.7)
    plt.title("Sifrelenmis Görüntü Histogramı")
    plt.xlabel("Piksel Değeri")
    plt.ylabel("Frekans")

    plt.tight_layout()
    plt.show()



compare_histograms( "original.png", "encrypted_image.png")

