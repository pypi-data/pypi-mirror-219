'''
author:        zlgecc <zlgecc@163.com>
date:          2023-07-11
'''
import hashlib
import uuid
import time
import jwt
import base64
from binascii import b2a_hex, a2b_hex

SECRET = "AIR5zymBz83DHjIj"

def random_id(number=16):
    random_uuid = uuid.uuid4()
    random_id = random_uuid.hex[:number]
    return random_id


def md5(string, encoding=True):
    s = string.encode("utf8") if encoding else string
    return hashlib.md5(s).hexdigest()


# base64 encoded decode
def base64_encode(data):
    encoded_bytes = base64.b64encode(data.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def base64_decode(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

# jwt 加密算法
def jwt_encode(data):
    """jwt加密"""
    data["ts"] = int(time.time())
    token = jwt.encode(data, SECRET, algorithm="HS256")
    return token


def jwt_decode(token):
    """jwt解密"""
    if not token:
        return False
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except Exception as e:
        return False


# AES 加密算法
def aes_decrypt(data, pad="zero"):
    from Crypto.Cipher import AES, DES

    """AES-128-CBC 解密"""
    real_data = base64.b64decode(data)
    # 获取加密后的字符串数据
    iv = md5(SECRET.encode(), encoding=False)[:16]
    cryptor = AES.new(SECRET.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
    decrypt_data = cryptor.decrypt(real_data)

    # 解密后的数据去除加密前添加的数据
    if pad == "zero":  # 去掉数据在转化前不足16位长度时添加的ASCII码为0编号的二进制字符
        return "".join([chr(i) for i in decrypt_data if i != 0])
    elif pad == "pkcs7":  # 去掉pkcs7模式中添加后面的字符
        return "".join([chr(i) for i in decrypt_data if i > 32])
    else:
        return "不存在此种数据填充方式"


def aes_encrypt(text, base=64):
    from Crypto.Cipher import AES, DES

    """AES-128-CBC 加密"""
    # 预处理,填充明文为16的倍数
    pad = 16 - len(text.encode("utf8")) % 16
    text = text + pad * chr(pad)
    text = text.encode("utf8")

    # 获取加密后的字符串数据
    iv = md5(SECRET.encode(), encoding=False)[:16]

    cryptor = AES.new(SECRET.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
    cipher_text = cryptor.encrypt(text)
    if base == 16:
        # 返回16进制密文
        return b2a_hex(cipher_text).decode("utf8")
    elif base == 64:
        # 返回base64密文
        return base64.b64encode(cipher_text).decode("utf8")


if __name__ == "__main__":
    secret = random_id(number=16)
    SECRET = secret
    print("///", secret, len(secret))

    
    e = aes_encrypt('{"name": "zlgecc"}')
    d = aes_decrypt(e)
    print(e, d)

    # DeAesCrypt(data=info_data.get('username'),key=info_data.get('aes_key')).decrypt_aes
