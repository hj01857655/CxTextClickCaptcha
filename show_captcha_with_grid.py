#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
显示验证码并标注坐标网格
"""

import sys
from PIL import Image, ImageDraw, ImageFont

def show_captcha_with_grid(image_path):
    """在图片上绘制坐标网格"""
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    width, height = img.size
    
    # 绘制网格（每 50 像素一条线）
    grid_size = 50
    
    # 竖线
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill='red', width=1)
        draw.text((x+2, 2), str(x), fill='red')
    
    # 横线
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill='red', width=1)
        draw.text((2, y+2), str(y), fill='red')
    
    # 保存
    output_path = image_path.replace('.jpg', '_grid.jpg')
    img.save(output_path)
    
    print(f"✅ 已生成带网格的图片: {output_path}")
    print(f"图片尺寸: {width}x{height}")
    print("\n请打开图片，根据网格估算坐标")
    print("提示：文字中心点的坐标")
    
    # 尝试打开图片
    try:
        import os
        os.startfile(output_path)
        print("✅ 已自动打开图片")
    except:
        print(f"请手动打开: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python show_captcha_with_grid.py <图片路径>")
        sys.exit(1)
    
    show_captcha_with_grid(sys.argv[1])
