# drive-quiz-site
一款以驾车闯关形式呈现的原创知识答题游戏
# 🚗 驾车闯关 · 知识答题游戏

> 一款以驾车闯关形式呈现的知识答题游戏。题库围绕戒色、《寿康宝鉴》、古代道德穿着规范与守心标准，答对才能通行，满 90 分开启下一关。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/Content-CC%20BY--SA%204.0-lightgrey.svg)](./LICENSE-CONTENT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6.svg)]()

---

## 📖 项目简介

“驾车闯关”是一款单机桌面答题游戏。玩家以“驾车闯关”的形式答题，**答对才能通行**。每关共 100 题（50 道选择题 + 50 道判断题），答对一题得一分，**单关满 90 分即可开启下一关**。

题库内容围绕以下主题构建：

- **戒色**：自律、节欲、远离诱惑的实践准则
- **《寿康宝鉴》**：清代典籍中的劝诫与修身内容
- **古代道德穿着规范**：西周至唐代的服饰礼制与史实
- **守心标准**：源自《左传》《孟子》、曾国藩修身准则等

游戏为原创独立实现，界面与逻辑均未复制任何受法律保护的专利代码。

---

## ✨ 功能特性

| 功能 | 说明 |
|---|---|
| 🎯 主题题库 | 戒色、《寿康宝鉴》、古代穿着规范、守心标准 |
| 🧮 100 分制 | 50 选择题 + 50 判断题，每题 1 分 |
| ✅ 90 分过关 | 单关满 90 分开启下一关，未达标可重挑战 |
| ⏯️ 随时控制 | 支持开始 / 暂停 / 停止，进度可控 |
| 🖥️ 独立 exe | 打包为 Windows 可执行文件，双击即运行 |
| 🔄 自动更新 | 启动时后台静默检查版本，不阻塞游戏 |
| 🌐 配套官网 | 纯静态展示页，可部署到任意静态托管平台 |

---

---

## 🚀 快速开始

### 方式一：直接下载 exe（普通用户）

1. 前往 [Releases](../../releases) 页面下载最新版 `驾车闯关.exe`
2. 双击运行，无需安装 Python 环境
3. 若杀毒软件误报，请添加信任（PyInstaller 打包单文件的常见现象）

### 方式二：从源码运行（开发者）

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/drive-quiz.git
cd drive-quiz

# 2. 安装依赖（仅需标准库，无需额外安装）
python --version   # 确认 Python 3.8+

# 3. 运行
python drive_quiz.py

##📦 打包为 exe
bash
# 安装 PyInstaller
pip install pyinstaller

# 打包（单文件 + 无控制台窗口）
pyinstaller --onefile --windowed --name 驾车闯关 drive_quiz.py
生成文件位于 dist/驾车闯关.exe。

📚 题库说明
每关随机抽取 25 道选择题 + 25 道判断题（共 50 题），每题 2 分制换算后满分 100 分

题库总数建议 ≥ 50 道选择题 + 50 道判断题，以保证关卡随机性

题目内容依据公开典籍与史料整理，古籍原文属公有领域，项目作者对整理与原创表述享有著作权（见 LICENSE-CONTENT）

欢迎通过 Issue / PR 补充题目，贡献时请注明依据出处

##🗂️ 项目结构
text
drive-quiz/
├── drive_quiz.py          # 游戏主程序（Tkinter）
├── site/                  # 配套官网（纯静态）
│   ├── index.html
│   ├── style.css
│   └── script.js
├── assets/                # 图标、截图、发布用 exe（可选）
├── LICENSE                # 代码许可（MIT）
├── LICENSE-CONTENT        # 题库内容许可（CC BY-SA 4.0）
├── README.md              # 本文件
├── CONTRIBUTING.md        # 贡献指南
├── CODE_OF_CONDUCT.md     # 行为准则
├── CHANGELOG.md           # 版本记录
├── SECURITY.md            # 安全说明
└── .gitignore             # Git 忽略规则



##🔄 自动更新配置
游戏内置轻量级版本检查，默认关闭。如需启用：

在服务器托管一个 version.json：

json
{
  "version": "1.0.1",
  "url": "https://your-server.com/驾车闯关-1.0.1.exe"
}

修改 drive_quiz.py 中的配置：

python
CURRENT_VERSION = "1.0.0"
UPDATE_URL = "https://your-server.com/version.json"

检查在后台线程中进行，更新服务器不可用时静默忽略，不影响游戏运行。

##🌐 网站部署
site/ 目录为纯静态页面，可部署到：

GitHub Pages：仓库 Settings → Pages → 选择分支

Netlify：拖拽文件夹到 https://app.netlify.com/drop

Vercel：导入仓库自动部署

任意虚拟主机：FTP 上传至网站根目录

exe 文件较大时可上传至网盘（如蓝奏云），修改下载按钮链接即可。

##🤝 贡献指南
欢迎提交 Issue 和 Pull Request！请先阅读 CONTRIBUTING.md。

##贡献方向：

📝 补充题库（须注明依据出处）

🐛 修复 Bug

✨ 新增功能

📖 完善文档

🌐 网站优化

##📄 许可证
本项目采用双许可证：

部分许可证说明
源代码（*.py、*.html、*.css、*.js）	MIT	可自由使用、修改、商用，保留版权声明
题库内容（题目、解析、整理文字）	CC BY-SA 4.0	须署名、以相同协议共享
古籍原文（《寿康宝鉴》《左传》《唐律疏议》等）属公有领域，不受上述许可限制。

## ⚖️ 免责与法律声明
原创声明：本项目界面、逻辑、题库整理均为原创独立实现，未复制任何受法律保护的专利代码。

专利风险：截至发布时，未检索到与本项目实现方式相同的已授权专利。若未来商业化并扩展到联机对战、车际通信等场景，建议另行进行专利排查。

内容性质：题库内容用于传统文化与修身知识的学习自测，不构成任何形式的医疗、心理或法律建议。

软件性质：本软件为单机程序，不收集、不上传用户数据。自动更新检查为可选功能。

使用风险：软件按“原样”提供，作者不对使用后果承担任何明示或暗示的担保责任。

### 🙏 致谢
《寿康宝鉴》（印光大师增订）—— 传统文化修身典籍

《左传》《孟子》《唐律疏议》等 —— 守心与服饰礼制史料来源

Python / Tkinter —— 运行环境与 GUI

PyInstaller —— exe 打包工具

<p align="center">若本项目对你有帮助，欢迎点一个 ⭐ Star</p> ```
