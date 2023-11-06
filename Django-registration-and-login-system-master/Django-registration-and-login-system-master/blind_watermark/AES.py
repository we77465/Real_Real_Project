from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

def encrypt(plaintext, key):
    key = get_fixed_key(key)  # 生成16字节的密钥
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext)  # 填充明文
    ciphertext = cipher.encrypt(padded_plaintext)
    return b64encode(ciphertext).decode('utf-8')

def decrypt(ciphertext, key):
    key = get_fixed_key(key)  # 生成16字节的密钥
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext_bytes = b64decode(ciphertext)
    decrypted_text = cipher.decrypt(ciphertext_bytes)
    return unpad(decrypted_text).decode('utf-8')

def get_fixed_key(key):
    # 确保密钥是16字节长度
    fixed_key = key.ljust(16, '\0')
    return fixed_key.encode('utf-8')

def pad(s):
    # 使用PKCS7填充方式，将字符串填充为16的倍数
    block_size = 16
    pad_size = block_size - len(s) % block_size
    padded_text = s + pad_size * chr(pad_size)
    return padded_text.encode('utf-8')

def unpad(s):
    # 去除PKCS7填充
    return s[:-ord(s[len(s)-1:])]
