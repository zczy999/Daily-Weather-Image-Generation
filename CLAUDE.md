# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

每日天气图片生成服务：通过 AI 查询城市天气，生成钩针玩偶风格的天气卡片图片，并通过邮件发送。

## 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 直接生成一张图片
python main.py

# 测试邮件发送（不生成图片）
python test_email.py

# 完整测试（生成图片 + 发邮件）
python test_full.py

# 启动定时任务
python scheduler.py

# 立即执行一次定时任务
python scheduler.py now

# Docker 部署
docker compose up -d --build
docker compose logs -f
docker compose down
```

## 架构

- `main.py` - 核心图片生成逻辑
  - `generate_weather_image(city)` - 主入口函数，返回 (图片路径, 天气信息, 地标名称)
  - `query_weather()` - 通过 AI 搜索天气网站获取天气
  - `generate_image()` - 调用 AI 生成钩针玩偶风格图片
  - `LANDMARKS` - 杭州地标列表，每次随机选择一个

- `scheduler.py` - 定时任务和邮件发送
  - `send_email()` - 发送带图片的 HTML 邮件
  - `daily_task()` - 每日任务入口
  - `run_scheduler()` - 启动 schedule 定时器

## 配置

所有配置通过 `.env` 文件管理，参考 `.env.example`：
- `OPENAI_API_KEY` / `OPENAI_BASE_URL` - AI API 配置
- `CITY` - 城市名称
- `SMTP_*` / `EMAIL_TO` - 邮件配置
- `SCHEDULE_TIME` - 定时执行时间 (24小时制)

## 注意事项

- AI 模型使用 `gemini-3-pro-preview`，通过自定义网关调用
- 需要 `extra_body={"refresh_session": True}` 参数确保获取实时天气
- 图片响应格式为 `{"type": "image_url", "image_url": {"url": "..."}}`
