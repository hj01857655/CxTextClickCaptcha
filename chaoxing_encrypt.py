#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超星登录加密实现（Python 版本）
根据 login.js 逆向还原

加密算法：AES-CBC
密钥：u2oh6Vu^HWe4_AES
IV：与密钥相同
编码：Base64
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

# 超星固定密钥
TRANSFER_KEY = "u2oh6Vu^HWe4_AES"

def encrypt_by_aes(message: str, key: str = TRANSFER_KEY) -> str:
    """
    AES-CBC 加密（与 JS 版本完全一致）
    
    参数:
        message: 明文（用户名或密码）
        key: 密钥（默认使用超星的固定密钥）
    
    返回:
        Base64 编码的密文
    """
    # 1. 将密钥和 IV 转为字节
    key_bytes = key.encode('utf-8')
    iv_bytes = key.encode('utf-8')  # IV = key（超星的实现）
    
    # 2. 创建 AES 加密器（CBC 模式）
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    
    # 3. 填充明文（PKCS7）
    message_bytes = message.encode('utf-8')
    padded_message = pad(message_bytes, AES.block_size)
    
    # 4. 加密
    encrypted = cipher.encrypt(padded_message)
    
    # 5. Base64 编码
    return base64.b64encode(encrypted).decode('utf-8')

if __name__ == '__main__':
    # 简单测试
    test_text = "test"
    encrypted = encrypt_by_aes(test_text)
    print(f"明文: {test_text}")
    print(f"密文: {encrypted}")
