# coding: utf-8
from Cipher_AES_Byte import Cipher_AES_Byte

akey = "abcdefgh12345678"
iv = None

cipher_method = "MODE_ECB"
pad_method = "PKCS5Padding"

'''
    key 为字节码
    text 为字节码
'''
def decrypt_text(key, text):
    cipher_aes = Cipher_AES_Byte(key , iv, cipher_method, pad_method)
    return cipher_aes.decrypt(text)

def encrypt_text(key, text):
    cipher_aes = Cipher_AES_Byte(key, iv, cipher_method, pad_method)
    return cipher_aes.encrypt(text)

if __name__=="__main__":
    text = "我爱小姐姐，可小姐姐不爱我 - -"
    cipher_text = encrypt_text(akey.encode("UTF-8"), text.encode("UTF-8"))
    encode_func = Cipher_AES_Byte.encode.get("base64")
    print(encode_func(cipher_text))
    print(cipher_text)
    text = decrypt_text(akey.encode("UTF-8"),  cipher_text)
    print(text )