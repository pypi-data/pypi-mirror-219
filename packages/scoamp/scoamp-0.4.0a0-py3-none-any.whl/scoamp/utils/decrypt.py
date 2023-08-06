import binascii

# pip install pycryptodome
from Crypto.Cipher import AES


def decrypt_aes256gcm(key: str, ciphertext: str) -> str:
    if len(key) == 32:
        key = key.encode()
    else:
        key = binascii.unhexlify(key)
    hex_ciphertext = binascii.unhexlify(ciphertext)

    iv = hex_ciphertext[:12]
    data = hex_ciphertext[12:-16]
    auth_tag = hex_ciphertext[-16:]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    dd = cipher.decrypt_and_verify(data, auth_tag)
    return dd.decode()
