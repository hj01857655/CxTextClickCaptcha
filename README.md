# 超星点击式验证码半自动化处理工具

> ⚠️ **免责声明**：本项目仅供学习和研究使用，请勿用于非法用途。使用本工具产生的任何后果由使用者自行承担。

## 📖 项目简介

本项目实现了超星（学习通）点击式验证码的**半自动化处理**，包括完整的登录流程。

**注意**：这不是全自动破解工具，验证码需要人工识别文字位置并手动输入坐标。

## ✨ 功能特性

- ✅ 完整的验证码协议逆向（基于 `captcha_load.min.js`）
- ✅ 自动获取验证码图片
- ✅ 生成带网格的辅助图片（方便定位坐标）
- ✅ 手动输入坐标后自动提交验证
- ✅ AES 加密实现（用户名和密码）
- ✅ 完整的登录流程（包括密码重置处理）
- ✅ 机构账号登录支持

## 🔧 技术细节

### 验证码流程

1. **获取服务器时间戳**：`/captcha/get/conf`
2. **生成参数**：
   - `captchaKey = md5(serverTime + random())`
   - `token = md5(serverTime + captchaId + type + captchaKey) + ':' + (serverTime + 300000)`
3. **获取验证码**：`/captcha/get/verification/image`
4. **人工识别**：查看图片，识别需要点击的文字位置
5. **手动输入坐标**：格式 `x1,y1;x2,y2;x3,y3`
6. **自动提交验证**：`/captcha/check/verification/result`

### 加密算法

- **算法**：AES-CBC
- **密钥**：`u2oh6Vu^HWe4_AES`
- **IV**：与密钥相同
- **编码**：Base64

### 登录流程

1. 处理验证码（需要手动输入坐标）
2. 加密用户名和密码
3. 提交登录请求（`/unitlogin` 用于机构账号）
4. 处理密码重置（如果需要）
5. 获取 Session 和 Cookies

## 📦 依赖安装

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 安装依赖
pip install requests pycryptodome pillow
```

## 🚀 使用方法

### 1. 机构账号登录

```bash
python chaoxing_login_with_captcha.py <用户名> <密码> <机构ID>
```

**示例**：
```bash
python chaoxing_login_with_captcha.py your_username your_password 2207
```

### 2. 泛雅账号登录（普通登录）

```bash
python chaoxing_login_fanya.py <用户名> <密码>
```

**示例**：
```bash
python chaoxing_login_fanya.py your_phone your_password
```

**流程**：
1. 自动获取验证码图片
2. 生成带网格的辅助图片（保存在 `captcha/` 目录）
3. 查看图片，识别需要点击的文字
4. 输入坐标（格式：`x1,y1;x2,y2;x3,y3`）
5. 自动完成后续登录流程

### 2. 单独处理验证码

```bash
python captcha_handler.py
```

### 3. 坐标辅助工具

```bash
python show_captcha_with_grid.py <图片路径>
```

生成带网格的图片，方便定位坐标。

## 📁 项目结构

```
.
├── chaoxing_login_with_captcha.py  # 机构账号登录（主脚本）
├── chaoxing_login_fanya.py         # 泛雅账号登录（普通登录）
├── captcha_handler.py              # 验证码处理核心
├── chaoxing_encrypt.py             # AES 加密实现
├── show_captcha_with_grid.py       # 坐标辅助工具
├── login.js                        # 登录页面 JS（参考）
├── captcha_load.min.js             # 验证码 JS（参考）
└── captcha/                        # 验证码图片缓存
```

## 🎯 核心文件说明

### chaoxing_login_with_captcha.py

机构账号登录流程，包括：
- 验证码处理（需要手动输入坐标）
- 用户名和密码加密
- 登录请求提交
- 密码重置处理
- Session 管理

### chaoxing_login_fanya.py

泛雅账号登录流程（普通登录），包括：
- 验证码处理（需要手动输入坐标）
- 用户名和密码加密
- 泛雅登录请求提交
- Session 管理

### captcha_handler.py

验证码处理核心，包括：
- 获取服务器时间戳
- 生成 captchaKey 和 token
- 获取验证码图片
- 提交验证坐标

### chaoxing_encrypt.py

AES 加密实现，用于加密用户名和密码。

### show_captcha_with_grid.py

生成带网格的验证码图片，方便定位坐标。

## 📝 坐标输入说明

### 坐标格式

```
x1,y1;x2,y2;x3,y3
```

- 每个坐标用逗号分隔 `x,y`
- 多个坐标用分号分隔 `;`
- 坐标顺序与需要点击的文字顺序一致

### 坐标定位技巧

1. 查看带网格的图片（`captcha/*_grid.jpg`）
2. 找到需要点击的文字
3. 记录文字中心点的坐标
4. 按顺序输入坐标

**示例**：

如果需要点击 "要"、"问"、"句" 三个字：
- "要" 在 (70, 80)
- "问" 在 (220, 50)
- "句" 在 (240, 80)

输入：`70,80;220,50;240,80`

## ⚠️ 注意事项

1. **不是全自动破解**：需要人工识别文字位置并输入坐标
2. **仅供学习研究**：请勿用于非法用途
3. **账号安全**：不要在公共场合使用真实账号测试
4. **验证码有效期**：token 有效期 5 分钟，请及时输入坐标
5. **机构 ID**：不同学校的机构 ID 不同，需要自行查找

## 🔍 如何获取机构 ID

1. 打开超星登录页面
2. 选择机构登录
3. 查看 URL 中的 `fid` 参数

**示例**：
```
https://passport2.chaoxing.com/login?fid=2207
```

机构 ID 为 `2207`

## 🛠️ 技术栈

- **Python 3.x**
- **requests** - HTTP 请求
- **pycryptodome** - AES 加密
- **Pillow** - 图片处理

## 📚 参考资料

- [超星验证码 JS](https://captcha.chaoxing.com/dist/captcha_load.min.js)
- [超星登录页面](https://passport2.chaoxing.com/login)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## ⚡ 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/hj01857655/CxTextCaptcha.git
cd CxTextCaptcha

# 2. 安装依赖
pip install requests pycryptodome pillow

# 3. 运行测试
python chaoxing_login_with_captcha.py your_username your_password 2207

# 4. 查看验证码图片
# 图片保存在 captcha/ 目录

# 5. 输入坐标
# 格式：x1,y1;x2,y2;x3,y3
```

## 🎉 成功示例

```
✅ 验证码处理成功
Validate: validate_GcXX5vewqE7DezKGlyvleKCnkTglvGpL_...

✅ 用户名已加密
✅ 密码已加密

✅ 成功跳过密码重置！

🎉 完整登录流程成功！
```

## 📞 联系方式

- GitHub: [@hj01857655](https://github.com/hj01857655)

---

**再次提醒**：本项目仅供学习和研究使用，请勿用于非法用途！
