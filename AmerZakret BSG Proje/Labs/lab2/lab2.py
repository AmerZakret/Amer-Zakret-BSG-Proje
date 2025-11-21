import random

def generate_keystream(length, seed):
    random.seed(seed)
    return [random.randint(0, 255) for _ in range(length)]

def block_encrypt_with_seed(text, seed, blocksize=4):
    cipher = ""
    keystream = generate_keystream(len(text), seed)

    for i, ch in enumerate(text):
        cipher += chr(ord(ch) ^ keystream[i])
    return cipher

def block_decrypt_with_seed(cipher, seed):
    keystream = generate_keystream(len(cipher), seed)
    text = ""
    for i, ch in enumerate(cipher):
        text += chr(ord(ch) ^ keystream[i])
    return text

def xor_str(a, b):
    result = ''
    for x, y in zip(a, b):
        result += chr(ord(x) ^ ord(y))
    return result

text1 = "Merhaba"
text2 = "Hellooo"
seed = 1234

sifreli1 = block_encrypt_with_seed(text1, seed)
sifreli2 = block_encrypt_with_seed(text2, seed)

print("Şifreli1:", [ord(c) for c in sifreli1])
print("Şifreli2:", [ord(c) for c in sifreli2])


cozulmus1 = block_decrypt_with_seed(sifreli1, seed)
cozulmus2 = block_decrypt_with_seed(sifreli2, seed)

print("Çözülmüş1:", cozulmus1)
print("Çözülmüş2:", cozulmus2)

xor_cipher = xor_str(sifreli1, sifreli2)
xor_plain = xor_str(text1, text2)

print("XOR(Şifreli1, Şifreli2):", [ord(c) for c in xor_cipher])
print("XOR(Orijinal1, Orijinal2):", [ord(c) for c in xor_plain])