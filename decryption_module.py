# decryption_module.py  

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  
from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives import padding  
import os  
  
def decrypt(encrypted_data, key):  
    # 假设key是一个bytes类型的密钥，并且encrypted_data也是bytes类型的加密数据  
    # 假设我们使用的是AES算法和CBC模式，并且数据是PKCS7填充的  
    backend = default_backend()  
    iv = encrypted_data[:16]  # 假设初始向量(IV)是加密数据的前16个字节  
    cipher_text = encrypted_data[16:]  # 实际的密文是去掉IV后的数据  
  
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)  
    decryptor = cipher.decryptor()  
  
    # 去除填充  
    unpadder = padding.PKCS7(128).unpadder()  
    decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()  
    decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()  
  
    # 返回解密后的数据  
    return decrypted_data
  
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  
from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives import padding  
import os  
  
def encrypt(decrypted_data, key):  
    # 假设key是一个bytes类型的密钥，decrypted_data是需要加密的bytes类型数据  
    # 生成一个随机的初始向量(IV)  
    iv = os.urandom(16)  
  
    # 选择一个后端  
    backend = default_backend()  
  
    # 假设我们使用AES算法和CBC模式，并且数据需要进行PKCS7填充  
    padder = padding.PKCS7(128).padder()  
    padded_data = padder.update(decrypted_data) + padder.finalize()  
  
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)  
    encryptor = cipher.encryptor()  
  
    # 执行加密  
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()  
  
    # 将IV和密文连接起来返回  
    encrypted_data = iv + cipher_text  
    return encrypted_data