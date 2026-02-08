# EasyDrop 后端（FastAPI + SQLite）

## 功能概览

当前后端已实现 MVP 主要能力：
- 管理端登录（JWT）
- 素材上传/查询/删除（本地磁盘存储）
- 设备注册/登录
- 播放单与投放任务管理
- 设备 manifest 动态生成
- 设备日志上报与查询
- 设备 WebSocket（hello / heartbeat / report）

## 初始化

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 运行

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 客户端后端地址配置说明

- `frontend`：可在登录页或控制台顶部直接设置并保存后端地址（默认 `http://127.0.0.1:8000`）
- `screen-web`：页面顶部可设置并保存后端地址，保存后会持久化到本地存储

## 默认账号

首次启动会自动创建管理员：
- 用户名：`admin`
- 密码：`admin123`

生产环境请配置以下环境变量：
- `ADMIN_INIT_USERNAME`
- `ADMIN_INIT_PASSWORD`
- `JWT_SECRET`

## 已实现 API

- `POST /api/auth/login`
- `POST /api/media/upload`
- `GET /api/media`
- `GET /api/media/{id}`
- `DELETE /api/media/{id}`
- `POST /api/devices/register`
- `POST /api/devices/login`
- `GET /api/devices`
- `GET /api/devices/{id}`
- `PUT /api/devices/{id}`
- `GET /api/devices/{id}/manifest`
- `POST /api/playlists`
- `GET /api/playlists`
- `GET /api/playlists/{id}`
- `PUT /api/playlists/{id}`
- `POST /api/playlists/{id}/items`
- `DELETE /api/playlists/items/{item_id}`
- `DELETE /api/playlist-items/{item_id}`
- `POST /api/campaigns`
- `GET /api/campaigns`
- `GET /api/campaigns/{id}`
- `PUT /api/campaigns/{id}`
- `POST /api/campaigns/{id}/targets`
- `DELETE /api/campaigns/targets/{target_id}`
- `DELETE /api/campaign-targets/{target_id}`
- `POST /api/logs/report`
- `GET /api/logs/devices/{device_id}`
- `WS /ws/device?token=DEVICE_TOKEN`

## 数据与存储路径

- 数据库：`/Users/yaojiaqi/Programs/EasyDrop/data/app.db`
- 素材目录：`/Users/yaojiaqi/Programs/EasyDrop/storage/media`
- 缩略图目录：`/Users/yaojiaqi/Programs/EasyDrop/storage/thumb`
- manifest 目录：`/Users/yaojiaqi/Programs/EasyDrop/storage/manifest`
- 静态访问前缀：`/static`
