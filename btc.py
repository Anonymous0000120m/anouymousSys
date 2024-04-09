import bitcoin

# 生成一个比特币私钥
private_key = bitcoin.random_key()

# 从私钥生成比特币地址
address = bitcoin.privkey_to_address(private_key)
print("Bitcoin Address:", address)
