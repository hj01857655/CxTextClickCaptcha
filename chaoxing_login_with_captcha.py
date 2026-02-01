#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超星机构账号登录 - 包含验证码处理（需要手动输入坐标）

注意：
1. 本脚本用于机构账号登录（unitlogin 接口）
2. 验证码是点击式验证码，需要人工识别文字位置并输入坐标
3. 不是全自动破解，而是半自动化流程
"""

import sys
import requests
from chaoxing_encrypt import encrypt_by_aes
from captcha_handler import ChaoxingCaptchaHandler

def get_captcha_validate():
    """
    获取验证码 validate（需要手动输入坐标）
    
    流程：
    1. 自动获取验证码图片
    2. 生成带网格的辅助图片
    3. 人工识别文字位置
    4. 手动输入坐标
    5. 自动提交验证
    """
    cracker = ChaoxingCaptchaHandler()
    
    print("\n" + "🎯" * 35)
    print("超星验证码处理（需要手动输入坐标）")
    print("🎯" * 35 + "\n")
    
    # 步骤 1-4：获取验证码
    server_time = cracker.step1_get_server_time()
    if not server_time:
        return None
    
    captcha_key, token = cracker.step2_generate_params(server_time)
    new_token, image_url, context = cracker.step3_get_captcha_image(captcha_key, token)
    if not new_token:
        return None
    
    image_path = cracker.step4_download_image(image_url)
    if not image_path:
        return None
    
    print(f"\n✅ 验证码已下载: {image_path}")
    print(f"需要点击的文字: {context}")
    
    # 生成带网格的图片
    print("\n生成带网格的图片...")
    import subprocess
    result = subprocess.run(
        ['python', 'show_captcha_with_grid.py', image_path],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    
    # 手动输入坐标
    print("\n" + "=" * 70)
    print("请查看带网格的图片，然后输入坐标")
    print("格式：x1,y1;x2,y2;x3,y3")
    print("=" * 70)
    
    coords_input = input("\n请输入坐标: ").strip()
    
    if not coords_input:
        print("❌ 未输入坐标")
        return None
    
    # 解析坐标
    click_points = []
    for coord in coords_input.split(';'):
        coord = coord.strip()
        if not coord:
            continue
        x, y = map(int, coord.split(','))
        click_points.append({"x": x, "y": y})
    
    print(f"\n使用坐标: {click_points}")
    
    # 提交验证
    validate = cracker.step5_verify_captcha(new_token, click_points)
    
    return validate

def login_with_captcha(username, password, fid):
    """
    机构账号完整登录流程
    
    Args:
        username: 机构账号用户名
        password: 密码（明文）
        fid: 机构 ID（学校/单位的唯一标识）
    
    Returns:
        dict: 登录结果
            - success: bool, 是否成功
            - session: requests.Session, 会话对象
            - cookies: dict, Cookie 字典
            - validate: str, 验证码 validate
            - uid: str, 用户 ID（如果有）
    """
    print("\n" + "=" * 70)
    print("超星机构账号登录")
    print("=" * 70)
    
    # 步骤 1：处理验证码（需要手动输入坐标）
    print("\n步骤 1: 处理验证码（需要手动输入坐标）...")
    validate = get_captcha_validate()
    
    if not validate:
        print("❌ 验证码处理失败")
        return None
    
    print(f"\n✅ 验证码处理成功")
    print(f"Validate: {validate}")
    
    # 步骤 2：加密用户名和密码
    print("\n步骤 2: 加密用户名和密码...")
    encrypted_uname = encrypt_by_aes(username)
    encrypted_pwd = encrypt_by_aes(password)
    print(f"✅ 用户名已加密")
    print(f"✅ 密码已加密")
    
    # 步骤 3：登录（机构账号登录）
    print("\n步骤 3: 提交登录（机构账号）...")
    
    login_url = "https://passport2.chaoxing.com/unitlogin"
    
    data = {
        "pid": "-1",
        "fid": fid,
        "uname": encrypted_uname,
        "password": encrypted_pwd,
        "refer": "https://i.chaoxing.com",
        "t": "true",
        "validate": validate,
        "hidecompletephone": "0",
        "doubleFactorLogin": "0",
        "forbidotherlogin": "0",
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
        result_type = result.get("type")
        
        if result_type == 2:
            # 需要重置密码或补充信息
            print("\n⚠️ 需要重置密码或补充信息")
            reset_url = result.get("url")
            
            from urllib.parse import parse_qs, urlparse
            
            parsed = urlparse(f"https://passport2.chaoxing.com{reset_url}")
            params = parse_qs(parsed.query)
            
            uid = params.get('uid', [''])[0]
            code = params.get('code', [''])[0]
            
            # 调用密码重置接口（跳过验证）
            print("\n尝试跳过密码重置...")
            reset_api_url = "https://passport2.chaoxing.com/pwd/fanyapwdreset"
            
            reset_data = {
                "uid": uid,
                "pid": "-1",
                "fid": fid,
                "code": code,
                "phone": "",
                "vercode": "",
                "validate": "",
                "refer": "https://i.chaoxing.com",
                "needPhoneCode": "0",
                "hidecompletephone": "0",
                "messageCode": "",
                "pwd": "",
                "loginTypeDetail": "",
                "pt": "",
                "uname": ""
            }
            
            reset_resp = session.post(reset_api_url, data=reset_data, headers=headers, timeout=10)
            reset_result = reset_resp.json()
            
            if reset_result.get("status"):
                print("\n✅ 成功跳过密码重置！")
                
                cookies = session.cookies.get_dict()
                
                return {
                    "success": True,
                    "session": session,
                    "cookies": cookies,
                    "validate": validate,
                    "uid": uid
                }
            else:
                print(f"\n❌ 跳过密码重置失败: {reset_result.get('msg2', '未知错误')}")
                return {
                    "success": False,
                    "response": reset_resp.text,
                    "validate": validate,
                    "need_reset": True,
                    "reset_url": reset_url
                }
        
        elif result_type == 1:
            # 登录成功
            print("\n✅ 登录成功！")
            
            cookies = session.cookies.get_dict()
            
            return {
                "success": True,
                "session": session,
                "cookies": cookies,
                "validate": validate
            }
        else:
            print(f"\n⚠️ 未知的响应类型: {result_type}")
            return {
                "success": False,
                "response": resp.text,
                "validate": validate
            }
    else:
        print(f"\n❌ 登录失败: {result.get('msg2', result.get('mes', '未知错误'))}")
        return {
            "success": False,
            "response": resp.text,
            "validate": validate
        }

if __name__ == '__main__':
    # 从命令行参数获取账号信息
    if len(sys.argv) >= 4:
        USERNAME = sys.argv[1]
        PASSWORD = sys.argv[2]
        FID = sys.argv[3]
    else:
        print("用法: python chaoxing_login_with_captcha.py <用户名> <密码> <机构ID>")
        print("示例: python chaoxing_login_with_captcha.py your_username your_password 2207")
        print("\n说明：")
        print("  - 用户名：机构账号用户名")
        print("  - 密码：账号密码")
        print("  - 机构ID：学校/单位的唯一标识（在登录页面 URL 中可以找到）")
        sys.exit(1)
    
    print("\n" + "🎯" * 35)
    print("超星机构账号登录")
    print("🎯" * 35)
    
    print(f"\n机构 ID: {FID}")
    print(f"用户名: {USERNAME}")
    
    result = login_with_captcha(USERNAME, PASSWORD, FID)
    
    print("\n" + "=" * 70)
    if result and result.get("success"):
        print("🎉 登录成功！")
        print("\n现在可以使用 session 访问超星的其他接口了")
    else:
        print("❌ 登录失败")
    print("=" * 70)
