import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

# AES ECB mode without IV

key = os.environ.get('CIPHER_PRIVATE_KEY')  # Must Be 16 char for AES128


def encrypt(raw):
    raw = pad(raw.encode(), 16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    encrypted_data = cipher.encrypt(raw)
    encrypted_data_hex = binascii.hexlify(encrypted_data).decode('utf-8')
    return encrypted_data_hex


def decrypt(enc):
    try:
        enc = binascii.unhexlify(enc.encode('utf-8'))
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(enc), 16)
        return decrypted.decode('utf-8', 'ignore')
    except (ValueError, TypeError):
        # Handle decryption errors, such as invalid input or incorrect padding
        return None
