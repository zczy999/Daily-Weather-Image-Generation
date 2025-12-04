FROM python:3.13-slim

WORKDIR /app

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY *.py .

# 设置编码
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8

CMD ["python", "scheduler.py"]
