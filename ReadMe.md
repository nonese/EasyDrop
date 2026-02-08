# EasyDrop 广告投放系统（MVP）

本项目目标是实现以下闭环：
用户上传素材 -> 服务器管理与分发 -> 屏幕客户端拉取/接收 -> 本地播放与日志上报。

## 目录结构

```text
/Users/yaojiaqi/Programs/EasyDrop
├── backend/           # FastAPI 服务端（已实现 MVP 核心）
├── frontend/          # 管理端 Vue（已初始化并接入后端 API）
├── screen-web/        # Web 屏幕端（最小可运行示例）
├── screen-android/    # Android 屏幕端（目录与说明已预留）
├── storage/           # 素材与清单存储
│   ├── media/
│   ├── thumb/
│   └── manifest/
└── data/
    └── app.db         # SQLite 数据库（运行后自动创建）
```

## 环境要求

- Python 3.10+（建议）
- Node.js 18+（用于前端 Vue）
- npm 9+
- Android Studio（用于 Android 客户端开发）

## 项目初始化

### 1. 初始化后端

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. 初始化前端（Vue 管理端）

`frontend/` 已是可运行项目，安装依赖即可：

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/frontend
npm install
```

### 3. 初始化屏幕 Web 端

`screen-web/` 已提供可运行示例（无需额外安装依赖），建议用静态服务器启动。

### 4. 初始化 Android 端

在 Android Studio 打开：
`/Users/yaojiaqi/Programs/EasyDrop/screen-android`

建议技术栈：Kotlin + ExoPlayer + WorkManager + OkHttp(WebSocket)。

## 运行方式

### 1. 启动后端服务

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

启动后地址：
- 服务首页：[http://127.0.0.1:8000](http://127.0.0.1:8000)
- OpenAPI 文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

默认管理员账号（首次启动自动创建）：
- 用户名：`admin`
- 密码：`admin123`

### 2. 启动前端管理端（Vue）

执行：

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/frontend
npm run dev
```

默认开发地址通常为：
- [http://127.0.0.1:5173](http://127.0.0.1:5173)

后端地址配置方式（前端页面内）：
- 登录页可输入并保存“后端地址”
- 控制台顶部也可随时修改并保存“后端地址”
- 默认值：`http://127.0.0.1:8000`

### 3. 启动屏幕 Web 客户端

方式一（推荐，使用 Python 简单静态服务）：

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/screen-web
python3 -m http.server 8081
```

打开：
- [http://127.0.0.1:8081](http://127.0.0.1:8081)

页面中填写后端地址（默认 `http://127.0.0.1:8000`），按顺序点击：
- 保存后端地址（会写入本地存储）
- 注册设备
- 登录设备
- 开始播放

### 4. 运行 Android 客户端

- 使用 Android Studio 打开 `screen-android/`
- 配置后端基地址（局域网请填服务端机器 IP）
- 运行到真机或模拟器

## 当前已实现范围

- 后端：鉴权、素材上传、设备注册登录、播放单/投放任务、manifest 生成、日志上报、设备 WS 心跳
- 屏幕 Web：设备注册登录、manifest 拉取、循环播放、日志上报
- 前端管理端：已完成登录、素材、设备、播放单、投放任务、日志模块
- Android 端：目录与开发说明预留

## 参考文档

- 后端详细说明：`/Users/yaojiaqi/Programs/EasyDrop/backend/README.md`
- 前端说明：`/Users/yaojiaqi/Programs/EasyDrop/frontend/README.md`
- 屏幕 Web 说明：`/Users/yaojiaqi/Programs/EasyDrop/screen-web/README.md`
- Android 说明：`/Users/yaojiaqi/Programs/EasyDrop/screen-android/README.md`
