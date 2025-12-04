# Daily Weather Image Generation

每日天气图片生成服务：通过 AI 查询城市天气，生成钩针玩偶风格的天气卡片图片，并通过邮件发送。

## 功能特点

- **实时天气查询**：通过 AI 搜索多个天气网站获取准确天气数据
- **钩针玩偶风格**：生成独特的针织/钩针玩偶风格天气卡片
- **城市地标展示**：每次随机选择一个城市地标作为背景
- **自动时间氛围**：根据当前时间自动调整图片光线和氛围
- **邮件推送**：支持将天气卡片通过邮件发送
- **定时任务**：支持每日定时自动执行
- **Docker 部署**：一键容器化部署

## 示例效果

生成的图片将展示：
- 钩针玩偶风格的城市地标
- 当日天气状况（晴/阴/雨/雪等）
- 温度信息
- 根据时间变化的背景氛围

## 快速开始

### 环境要求

- Python 3.10+
- 支持 OpenAI API 兼容格式的 AI 服务

### 安装

```bash
# 克隆项目
git clone <repository-url>
cd Daily-Weather-Image-Generation

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 配置

复制示例配置文件并填写：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# OpenAI API 配置
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=http://your_api_gateway/v1

# 城市配置
CITY=杭州市

# 邮件配置
SMTP_HOST=smtp.qq.com
SMTP_PORT=465
SMTP_USER=your_email@qq.com
SMTP_PASSWORD=your_auth_code
EMAIL_TO=recipient@example.com

# 定时配置 (24小时制)
SCHEDULE_TIME=08:00
```

**邮件服务配置参考**：
| 邮箱服务 | SMTP 服务器 | 端口 |
|---------|------------|------|
| QQ 邮箱 | smtp.qq.com | 465 |
| 163 邮箱 | smtp.163.com | 465 |
| Gmail | smtp.gmail.com | 587 |

## 使用方法

### 直接生成图片

```bash
python main.py
```

生成的图片保存在 `generated_images/` 目录下。

### 测试邮件发送

```bash
python test_email.py
```

仅测试邮件发送功能，不生成图片。

### 完整测试

```bash
python test_full.py
```

生成图片并发送邮件。

### 启动定时任务

```bash
python scheduler.py
```

根据 `SCHEDULE_TIME` 配置每日自动执行。

### 立即执行定时任务

```bash
python scheduler.py now
```

## Docker 部署

### 使用 Docker Compose（推荐）

```bash
# 构建并启动
docker compose up -d --build

# 查看日志
docker compose logs -f

# 停止服务
docker compose down
```

### 手动 Docker 构建

```bash
# 构建镜像
docker build -t daily-weather-image .

# 运行容器
docker run -d \
  --name daily-weather-image \
  --env-file .env \
  -v ./generated_images:/app/generated_images \
  -e TZ=Asia/Shanghai \
  daily-weather-image
```

## 项目结构

```
.
├── main.py              # 核心图片生成逻辑
├── scheduler.py         # 定时任务和邮件发送
├── test_email.py        # 邮件发送测试
├── test_full.py         # 完整流程测试
├── requirements.txt     # Python 依赖
├── Dockerfile           # Docker 镜像配置
├── docker-compose.yml   # Docker Compose 配置
├── .env.example         # 环境变量示例
└── generated_images/    # 生成的图片目录
```

## 技术实现

### 天气查询

使用 AI 搜索以下天气网站获取实时天气数据：
- 中国天气网 (weather.com.cn)
- 墨迹天气 (tianqi.moji.com)
- 和风天气 (qweather.com)

### 图片生成

通过精心设计的 Prompt，生成具有以下特点的图片：
- **钩针玩偶风格**：所有元素以针织/钩针玩偶形式呈现
- **天气表现**：根据实际天气展示相应的视觉效果
- **时间氛围**：根据当前时间调整光线和色调
- **城市地标**：展示配置城市的特色地标

### 支持的地标（杭州）

西湖断桥、雷峰塔、三潭印月、灵隐寺、西溪湿地、钱塘江大桥、六和塔、苏堤春晓、平湖秋月、曲院风荷、花港观鱼、柳浪闻莺、南屏晚钟、双峰插云、宝石山、湖滨步行街、河坊街、南宋御街、京杭大运河、拱宸桥

## 注意事项

- AI 模型默认使用 `gemini-3-pro-preview`，需要支持图片生成的 AI 服务
- 需要设置 `extra_body={"refresh_session": True}` 确保获取实时天气
- 邮件密码请使用授权码而非登录密码
- 生成的图片为 9:16 竖版比例，适合手机壁纸

## License

MIT License
