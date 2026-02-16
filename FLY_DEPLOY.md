# Fly.io 部署指南（按量计费 PAYG）

## 前置条件

1. 安装 flyctl：`brew install flyctl`（若 Homebrew 有权限问题，见 [fly.io 官方安装](https://fly.io/docs/hands-on/install-flyctl/)）
2. 登录：`fly auth login`

## 首次部署步骤

### 1. 创建并部署后端

```bash
cd backend
fly launch --no-deploy --name dingkwang-backend
fly scale vm shared-cpu-1x --memory 256
fly secrets set ANTHROPIC_API_KEY=你的Anthropic_API_Key
fly deploy
cd ..
```

### 2. 创建并部署前端

```bash
cd frontend
fly launch --no-deploy --name dingkwang-site
fly scale vm shared-cpu-1x --memory 256
fly deploy
cd ..
```

> 若 app 名已被占用，可改用 `dingkwang-backend-xxx` 等，并同步修改 `frontend/fly.toml` 中的 `NEXT_PUBLIC_API_URL` build arg。

## 后续更新部署

```bash
# 后端
cd backend && fly deploy && cd ..

# 前端
cd frontend && fly deploy && cd ..
```

## 验收

```bash
fly status -a dingkwang-backend
fly status -a dingkwang-site
fly logs -a dingkwang-backend
fly logs -a dingkwang-site
```

- 后端健康检查：`curl https://dingkwang-backend.fly.dev/health`
- 前端：访问 `https://dingkwang-site.fly.dev`

## 配置说明

- **shared-cpu-1x + 256MB**：最低配置
- **min_machines_running = 0**：空闲自动停机
- **auto_stop_machines = "stop" + auto_start_machines = true**：有请求时自动启动
- 应用监听 `0.0.0.0:8080`，Fly 负责 80/443 转发

## 注意事项

- 冷启动：`min_machines_running=0` 时，首次请求会有几秒延迟
- 不要使用 Volume（会持续计费）
- 不要开启 dedicated IPv4（额外计费）
