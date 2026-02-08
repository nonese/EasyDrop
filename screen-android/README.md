# Android 屏幕客户端

当前目录为 Android 客户端预留目录。

## 建议技术栈

- Kotlin
- ExoPlayer
- WorkManager
- OkHttp（HTTP + WebSocket）

## 初始化方式

1. 使用 Android Studio 打开目录：
`/Users/yaojiaqi/Programs/EasyDrop/screen-android`
2. 创建项目或同步已有 Gradle 配置。
3. 配置后端基地址（开发环境通常为 `http://<服务端IP>:8000`）。

补充：
- 当前 `frontend` 与 `screen-web` 均已支持页面内直接设置后端地址并保存。
- Android 端建议同样提供“后端地址设置页”并持久化（SharedPreferences）。

## MVP 功能建议

- 设备注册/登录
- WebSocket 心跳
- 拉取 manifest
- 素材下载与本地缓存
- ExoPlayer 循环播放
- 播放日志上报
