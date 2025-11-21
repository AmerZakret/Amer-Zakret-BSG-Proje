def xor_str(a, b):
    result = ''
    for x, y in zip(a, b):
        result += chr(ord(x) ^ ord(y))
    return result

def block_encrypt(text, key, blocksize=4):
    cipher = ""
    for i in range(0, len(text), blocksize):
        block = text[i:i + blocksize] 

        while len(block) < blocksize:
            block += "-"

        for j in range(blocksize):
            cipher += chr(ord(block[j]) ^ ord(key[j % len(key)]))
    
    return cipher


text1 = "Merhaba"
text2 = "Hellooo"
key = "KEY2233"

sifreli = block_encrypt(text1, key)
sifreli2 = block_encrypt(text2, key)

print("Şifreli:", [ord(c) for c in sifreli])
print("Şifreli2:", [ord(c) for c in sifreli2])

print("XOR Sonucu:", [ord(c) for c in xor_str(sifreli, sifreli2)])
print("XOR Sonucu:", [ord(c) for c in xor_str(text1,text2)])