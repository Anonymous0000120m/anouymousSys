from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA1
import getpass
from Crypto.PublicKey import ECC

def generate_keys():
    # 提示用户输入密码，并隐藏输入
    password = getpass.getpass(prompt="Enter passphrase: ")

    # 将密码转换为字节
    password_bytes = password.encode('utf-8')

    # 使用 PBKDF2 导出密钥
    key = PBKDF2(password_bytes, b'', dkLen=16, count=1000, hmac_hash_module=SHA1)

    # 生成 ECC 密钥对
    key_pair = ECC.generate(curve='P-256')

    # 保存私钥到文件
    with open('private_key.pem', 'wb') as f:
        f.write(key_pair.export_key(format='PEM', protection="PBKDF2WithHMAC-SHA1AndAES128-CBC", passphrase=key))

    # 保存公钥到文件
    with open('public_key.pem', 'wb') as f:
        f.write(key_pair.public_key().export_key(format='PEM'))

    print("Keys generated and saved successfully.")

# 生成密钥对
generate_keys()
