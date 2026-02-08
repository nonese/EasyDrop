# 前端管理端（Vue3）

该目录已初始化为可运行的 Vue3 + Vite + TypeScript + Pinia + Vue Router 项目，并已接入后端 API。

## 功能

- 管理员登录（`/api/auth/login`）
- 素材管理（上传/列表/删除）
- 设备管理（列表/查看 manifest）
- 播放单管理（创建/添加项/删除项）
- 投放任务管理（创建/绑定设备）
- 播放日志查询（按设备最近 100 条）

## 初始化

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/frontend
npm install
```

## 运行

```bash
cd /Users/yaojiaqi/Programs/EasyDrop/frontend
npm run dev
```

默认访问地址：
- [http://127.0.0.1:5173](http://127.0.0.1:5173)

## 构建

```bash
npm run build
npm run preview
```

## 后端地址配置

默认后端地址为：
- `http://127.0.0.1:8000`

你有两种方式修改后端地址：

1. 页面内配置（推荐）
- 登录页可输入并保存后端地址
- 进入控制台后，顶部也可修改并保存
- 地址会保存在浏览器本地存储，刷新页面后仍生效

2. 环境变量配置（初始化默认值）
- 在 `frontend/.env` 中配置：

```env
VITE_API_BASE=http://你的后端地址:8000
```

可参考模板文件：
- `/Users/yaojiaqi/Programs/EasyDrop/frontend/.env.example`

## 设计风格说明

页面已采用“现代化 + 苹果毛玻璃 + 淡蓝色调”：
- 淡蓝渐变背景 + 光晕层
- 卡片式毛玻璃（`backdrop-filter`）
- 圆角、柔和阴影、蓝色渐变主按钮
- 响应式布局（桌面/移动）
