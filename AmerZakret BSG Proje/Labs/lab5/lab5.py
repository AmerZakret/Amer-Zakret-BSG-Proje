from PIL import Image
import numpy as np


original = np.array(Image.open("Lena.png").convert("RGB"))
encoded  = np.array(Image.open("GündüzA.png").convert("RGB"))


R_original = original[:, :, 0]
R_encoded  = encoded[:, :, 0]

bits = (R_encoded & 1).flatten()


length_bits = bits[:32]
length = int("".join(str(b) for b in length_bits), 2)
print("Mesaj uzunluğu (byte):", length)



message_bits = bits[32:32 + length * 8]
message_bytes = np.packbits(message_bits)
message = message_bytes.tobytes().decode("utf-8")
print("Gizli mesaj:", message)
