# EasyDrop 广告投放系统（MVP）

本项目已跑通核心闭环：
素材上传 -> 服务端管理与分发 -> 屏幕端拉取播放 -> 播放日志上报。

## 最新项目进度

- `backend`：已完成并可用
- `frontend`：已完成并可用
- `screen-web`：已完成并可用
- `screen-android`：目录与方案已预留，待开发

## 目录结构

```text
/Users/yaojiaqi/Programs/EasyDrop
├── backend/           # FastAPI 服务端（MVP 已完成）
├── frontend/          # Vue3 管理端（MVP 已完成）
├── screen-web/        # Web 屏幕端（MVP 已完成）
├── screen-android/    # Android 屏幕端（待开发）
├── storage/           # 素材与清单存储
│   ├── media/
│   ├── thumb/
│   └── manifest/
└── data/
    └── app.db         # SQLite 数据库（运行后自动创建）
```

## 环境要求

- Python 3.10+（后端、screen-web 静态服务）
- Node.js 18+ / npm 9+（前端）
- Android Studio（仅 Android 端开发时需要）

## 快速开始

### 1. 启动后端

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

后端地址：
- 服务首页：[http://127.0.0.1:8000](http://127.0.0.1:8000)
- API 文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

默认管理员账号（首次启动自动创建）：
- 用户名：`admin`
- 密码：`admin123`

### 2. 启动管理端（frontend）

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/frontend
npm install
npm run dev
```

默认地址：
- [http://127.0.0.1:5173](http://127.0.0.1:5173)

说明：
- 登录页和控制台顶部都可设置并保存后端地址
- 默认后端地址为 `http://127.0.0.1:8000`

### 3. 启动屏幕 Web 端（screen-web）

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/screen-web
python3 -m http.server 8081
```

访问地址：
- [http://127.0.0.1:8081](http://127.0.0.1:8081)

页面操作顺序：
1. 保存后端地址
2. 注册设备
3. 登录设备
4. 开始播放

## 当前已实现能力

### backend

- 管理员登录（JWT）
- 素材上传/查询/删除
- 设备注册/登录
- 播放单与投放任务管理
- 设备 manifest 动态生成
- 日志上报与查询
- 设备 WebSocket（hello / heartbeat / report）

### frontend

- 管理员登录
- 素材管理
- 设备管理
- 播放单管理
- 投放任务管理
- 播放日志查询

### screen-web

- 设备注册/登录
- manifest 拉取与版本检测
- 视频/图片循环播放
- 播放日志上报
- WebSocket hello/heartbeat

### screen-android

- 当前为预留目录
- 已有技术方案建议，尚未进入实现阶段

## 子项目文档

- 后端：`/Users/yaojiaqi/Programs/EasyDrop/backend/README.md`
- 前端：`/Users/yaojiaqi/Programs/EasyDrop/frontend/README.md`
- 屏幕 Web：`/Users/yaojiaqi/Programs/EasyDrop/screen-web/README.md`
- Android：`/Users/yaojiaqi/Programs/EasyDrop/screen-android/README.md`
