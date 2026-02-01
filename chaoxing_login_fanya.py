#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超星泛雅账号登录（普通账号密码登录）

注意：
1. 本脚本用于普通账号登录（fanyalogin 接口）
2. 不需要验证码（或验证码可选）
3. 直接用户名密码登录
"""

import sys
import requests
from chaoxing_encrypt import encrypt_by_aes

def login_fanya(username, password):
    """
    泛雅账号登录
    
    Args:
        username: 账号（手机号/邮箱/用户名）
        password: 密码（明文）
    
    Returns:
        dict: 登录结果
            - success: bool, 是否成功
            - session: requests.Session, 会话对象
            - cookies: dict, Cookie 字典
    """
    print("\n" + "=" * 70)
    print("超星泛雅账号登录")
    print("=" * 70)
    
    # 步骤 1：加密用户名和密码
    print("\n步骤 1: 加密用户名和密码...")
    encrypted_uname = encrypt_by_aes(username)
    encrypted_pwd = encrypt_by_aes(password)
    print(f"✅ 用户名已加密")
    print(f"✅ 密码已加密")
    
    # 步骤 2：登录（泛雅登录）
    print("\n步骤 2: 提交登录...")
    
    login_url = "https://passport2.chaoxing.com/fanyalogin"
    
    data = {
        "fid": "-1",
        "uname": encrypted_uname,
        "password": encrypted_pwd,
        "refer": "https://i.chaoxing.com",
        "t": "true",
        "forbidotherlogin": "0",
        "validate": "",
        "doubleFactorLogin": "0",
        "independentId": "0",
        "independentNameId": "0"
    }
    
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://passport2.chaoxing.com/login"
    }
    
    session = requests.Session()
    resp = session.post(login_url, data=data, headers=headers, timeout=10)
    
    print(f"\n[+] 响应状态码: {resp.status_code}")
    
    # 检查登录结果
    result = resp.json()
    
    if result.get("status"):
        print("\n✅ 登录成功！")
        
        cookies = session.cookies.get_dict()
        
        return {
            "success": True,
            "session": session,
            "cookies": cookies
        }
    else:
        print(f"\n❌ 登录失败: {result.get('msg2', result.get('mes', '未知错误'))}")
        return {
            "success": False,
            "response": resp.text
        }

if __name__ == '__main__':
    # 从命令行参数获取账号信息
    if len(sys.argv) >= 3:
        USERNAME = sys.argv[1]
        PASSWORD = sys.argv[2]
    else:
        print("用法: python chaoxing_login_fanya.py <用户名> <密码>")
        print("示例: python chaoxing_login_fanya.py your_username your_password")
        print("\n说明：")
        print("  - 用户名：手机号/邮箱/用户名")
        print("  - 密码：账号密码")
        sys.exit(1)
    
    print("\n" + "🎯" * 35)
    print("超星泛雅账号登录")
    print("🎯" * 35)
    
    print(f"\n用户名: {USERNAME}")
    
    result = login_fanya(USERNAME, PASSWORD)
    
    print("\n" + "=" * 70)
    if result and result.get("success"):
        print("🎉 登录成功！")
        print("\n现在可以使用 session 访问超星的其他接口了")
    else:
        print("❌ 登录失败")
    print("=" * 70)
