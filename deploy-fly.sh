#!/bin/bash
# Fly.io 部署脚本 - 按量计费 (PAYG) 省钱配置
# 使用前请先: brew install flyctl && fly auth login

set -e

BACKEND_APP="dingkwang-backend"
FRONTEND_APP="dingkwang-site"

echo "=== 1. 部署后端 (FastAPI) ==="
cd backend
fly scale vm shared-cpu-1x --memory 256 -a "$BACKEND_APP" 2>/dev/null || true
fly deploy -a "$BACKEND_APP"
cd ..

echo ""
echo "=== 2. 设置后端密钥 (首次部署必须) ==="
echo "运行: fly secrets set ANTHROPIC_API_KEY=你的密钥 -a $BACKEND_APP"
echo "设置后如需重启: fly apps restart $BACKEND_APP"
echo ""

echo "=== 3. 部署前端 (Next.js) ==="
cd frontend
fly scale vm shared-cpu-1x --memory 256 -a "$FRONTEND_APP" 2>/dev/null || true
fly deploy -a "$FRONTEND_APP"
cd ..

echo ""
echo "=== 4. 验收 ==="
fly status -a "$BACKEND_APP"
echo ""
fly status -a "$FRONTEND_APP"
echo ""
echo "后端: https://$BACKEND_APP.fly.dev/health"
echo "前端: https://$FRONTEND_APP.fly.dev"
