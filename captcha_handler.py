#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超星点击式验证码处理 - 协议级实现

完整流程（根据 captcha_load.min.js 逆向）：
1. 调用 /captcha/get/conf 获取服务器时间戳 t
2. 使用 t 生成 captchaKey 和 token
3. 调用 /captcha/get/verification/image 获取验证码和新 token
4. 下载验证码图片
5. 识别文字位置（需要手动输入坐标）
6. 调用 /captcha/check/verification/result 提交验证
7. 获取 validate 用于登录

注意：本脚本不是全自动破解，需要人工识别文字位置并输入坐标
"""

import sys
import requests
import json
import time
import hashlib
import random
from pathlib import Path

class ChaoxingCaptchaHandler:
    """超星点击式验证码处理类"""
    
    def __init__(self):
        self.session = requests.Session()
        self.captcha_id = "GcXX5vewqE7DezKGlyvleKCnkTglvGpL"  # 超星验证码固定 ID
        self.captcha_type = "textclick"  # 点击式验证码
        self.base_url = "https://captcha.chaoxing.com"
        
        # 设置基础 Cookie（可选）
        self.session.cookies.set("route", "c873910f23fdbb50ba156beee2b1b2db")
        self.session.cookies.set("source", "")
        
        Path("captcha").mkdir(exist_ok=True)
        
        self.headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "script",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://passport2.chaoxing.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def md5(self, text):
        """MD5 哈希"""
        return hashlib.md5(str(text).encode()).hexdigest()
    
    def random_num(self):
        """生成随机数（6位）"""
        return random.randint(100000, 999999)
    
    def generate_iv(self):
        """生成 iv"""
        timestamp = str(int(time.time() * 1000))
        random_str = str(self.random_num())
        raw_str = f"{self.captcha_id}{self.captcha_type}{timestamp}{random_str}"
        return self.md5(raw_str)
    
    def step1_get_server_time(self):
        """步骤 1: 获取服务器时间戳"""
        print("=" * 70)
        print("步骤 1: 获取服务器时间戳")
        print("=" * 70)
        
        url = f"{self.base_url}/captcha/get/conf"
        
        params = {
            "callback": "cx_captcha_function",
            "captchaId": self.captcha_id,
            "_": str(int(time.time() * 1000))
        }
        
        resp = self.session.get(url, params=params, headers=self.headers, timeout=10)
        
        # 解析 JSONP
        json_str = resp.text[resp.text.find('(')+1:resp.text.rfind(')')]
        data = json.loads(json_str)
        
        server_time = data.get('t')
        print(f"✅ 服务器时间戳: {server_time}")
        
        return server_time
    
    def step2_generate_params(self, server_time):
        """步骤 2: 生成 captchaKey 和 token"""
        print("\n" + "=" * 70)
        print("步骤 2: 生成 captchaKey 和 token")
        print("=" * 70)
        
        # captchaKey = md5(serverTime + random)
        random_num = self.random_num()
        captcha_key = self.md5(f"{server_time}{random_num}")
        
        # token = md5(serverTime + captchaId + type + captchaKey) + ':' + (parseInt(serverTime) + 300000)
        token_hash = self.md5(f"{server_time}{self.captcha_id}{self.captcha_type}{captcha_key}")
        token = f"{token_hash}:{int(server_time) + 300000}"
        
        print(f"✅ 参数生成成功")
        
        return captcha_key, token
    
    def step3_get_captcha_image(self, captcha_key, token):
        """步骤 3: 获取验证码图片"""
        print("\n" + "=" * 70)
        print("步骤 3: 获取验证码图片")
        print("=" * 70)
        
        url = f"{self.base_url}/captcha/get/verification/image"
        
        # 生成 iv
        iv = self.generate_iv()
        
        # 登录页面 URL
        referer_url = "https://passport2.chaoxing.com/login?loginType=3&newversion=true&fid=-1"
        
        params = {
            "callback": "cx_captcha_function",
            "captchaId": self.captcha_id,
            "type": self.captcha_type,
            "version": "1.1.20",
            "captchaKey": captcha_key,
            "token": token,
            "referer": referer_url,
            "iv": iv,
            "_": str(int(time.time() * 1000))
        }
        
        resp = self.session.get(url, params=params, headers=self.headers, timeout=10)
        
        # 解析 JSONP
        json_str = resp.text[resp.text.find('(')+1:resp.text.rfind(')')]
        data = json.loads(json_str)
        
        if data.get('token'):
            new_token = data['token']
            image_url = data.get('imageVerificationVo', {}).get('originImage')
            context = data.get('imageVerificationVo', {}).get('context')
            
            print(f"✅ 获取成功！")
            print(f"图片 URL: {image_url}")
            print(f"需要点击的文字: {context}")
            
            return new_token, image_url, context
        else:
            print(f"❌ 获取失败")
            return None, None, None
    
    def step4_download_image(self, image_url):
        """步骤 4: 下载验证码图片"""
        print("\n" + "=" * 70)
        print("步骤 4: 下载验证码图片")
        print("=" * 70)
        
        # 图片下载需要特定的 headers
        image_headers = {
            "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "accept-language": "zh-CN,zh;q=0.9",
            "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "image",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://passport2.chaoxing.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        resp = self.session.get(image_url, headers=image_headers, timeout=10)
        
        if resp.status_code == 200:
            filename = f"captcha/captcha_{int(time.time())}.jpg"
            with open(filename, "wb") as f:
                f.write(resp.content)
            
            print(f"✅ 图片已保存: {filename}")
            return filename
        else:
            print(f"❌ 下载失败: {resp.status_code}")
            return None
    
    def step5_verify_captcha(self, token, click_points):
        """步骤 5: 提交验证"""
        print("\n" + "=" * 70)
        print("步骤 5: 提交验证")
        print("=" * 70)
        
        url = f"{self.base_url}/captcha/check/verification/result"
        
        # 生成 iv
        iv = self.generate_iv()
        
        params = {
            "callback": "cx_captcha_function",
            "captchaId": self.captcha_id,
            "type": self.captcha_type,
            "token": token,
            "textClickArr": json.dumps(click_points, separators=(',', ':')),
            "coordinate": "[]",
            "runEnv": "10",
            "version": "1.1.20",
            "t": "a",
            "iv": iv,
            "_": str(int(time.time() * 1000))
        }
        
        resp = self.session.get(url, params=params, headers=self.headers, timeout=10)
        
        # 解析响应
        json_str = resp.text[resp.text.find('(')+1:resp.text.rfind(')')]
        data = json.loads(json_str)
        
        if data.get('result'):
            extra_data = json.loads(data.get('extraData', '{}'))
            validate = extra_data.get('validate')
            print(f"✅ 验证成功！")
            print(f"Validate: {validate}")
            return validate
        else:
            print(f"❌ 验证失败: {data.get('msg')}")
            return None
    
    def run(self):
        """运行完整流程"""
        print("\n" + "🎯" * 35)
        print("超星点击式验证码处理")
        print("🎯" * 35 + "\n")
        
        # 步骤 1: 获取服务器时间戳
        server_time = self.step1_get_server_time()
        if not server_time:
            return None
        
        # 步骤 2: 生成参数
        captcha_key, token = self.step2_generate_params(server_time)
        
        # 步骤 3: 获取验证码
        new_token, image_url, context = self.step3_get_captcha_image(captcha_key, token)
        if not new_token:
            return None
        
        # 步骤 4: 下载图片
        image_path = self.step4_download_image(image_url)
        if not image_path:
            return None
        
        # 步骤 5: 手动输入坐标
        print(f"\n需要点击的文字: {context}")
        print("\n请查看图片，然后输入坐标")
        print("格式：x1,y1;x2,y2;x3,y3")
        
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
        
        # 步骤 6: 提交验证
        validate = self.step5_verify_captcha(new_token, click_points)
        
        return validate

if __name__ == '__main__':
    cracker = ChaoxingCaptchaHandler()
    validate = cracker.run()
    
    print("\n" + "=" * 70)
    if validate:
        print("🎉 验证码处理成功！")
        print(f"Validate: {validate}")
        print("\n现在可以用这个 validate 登录了！")
    else:
        print("❌ 验证码处理失败")
    print("=" * 70)
