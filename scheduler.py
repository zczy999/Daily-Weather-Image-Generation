import os
import smtplib
import time
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import schedule
from dotenv import load_dotenv

from main import generate_weather_image

# 加载环境变量
load_dotenv()


def send_email(image_path, weather_info, landmark, city="杭州市"):
    """
    发送天气图片邮件

    Args:
        image_path: 图片文件路径
        weather_info: 天气信息
        landmark: 地标名称
        city: 城市名称
    """
    # 读取邮件配置
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 465))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_to = os.getenv("EMAIL_TO")

    if not all([smtp_host, smtp_user, smtp_password, email_to]):
        print("邮件配置不完整，请检查 .env 文件")
        return False

    # 创建邮件
    msg = MIMEMultipart("related")
    msg["From"] = smtp_user
    msg["To"] = email_to
    msg["Subject"] = f"【{city}天气】{datetime.now().strftime('%Y年%m月%d日')} - {landmark}"

    # 判断是否有图片
    has_image = image_path and os.path.exists(image_path)

    # 邮件正文（图片嵌入显示）
    image_html = '<img src="cid:weather_image" style="max-width: 100%; border-radius: 12px; margin: 15px 0;">' if has_image else ""

    html_content = f"""
    <html>
    <body style="font-family: 'Microsoft YaHei', Arial, sans-serif; padding: 20px; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #333;">🌤️ {city}今日天气</h2>
        <p style="color: #666;">📍 今日地标：<strong>{landmark}</strong></p>
        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <pre style="margin: 0; white-space: pre-wrap;">{weather_info}</pre>
        </div>
        {image_html}
        <p style="color: #999; font-size: 12px;">
            生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    # 嵌入图片到正文
    if has_image:
        with open(image_path, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", "<weather_image>")
            img.add_header("Content-Disposition", "inline",
                           filename=os.path.basename(image_path))
            msg.attach(img)

    # 发送邮件
    try:
        print(f"正在发送邮件到 {email_to}...")
        server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, email_to.split(","), msg.as_string())
        print("邮件发送成功！")
        try:
            server.quit()
        except Exception:
            pass  # 忽略关闭连接时的错误
        return True
    except Exception as e:
        print(f"邮件发送失败：{e}")
        return False


def daily_task():
    """每日定时任务"""
    print(f"\n{'='*50}")
    print(f"开始执行定时任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    # 生成图片
    city = os.getenv("CITY", "杭州市")
    image_path, weather_info, landmark = generate_weather_image(city)

    if image_path:
        # 发送邮件
        send_email(image_path, weather_info, landmark, city)
    else:
        print("图片生成失败，跳过发送邮件")

    print(f"\n{'='*50}")
    print(f"定时任务执行完毕")
    print(f"{'='*50}\n")


def run_scheduler():
    """运行定时调度器"""
    schedule_time = os.getenv("SCHEDULE_TIME", "08:00")

    print(f"定时任务已启动")
    print(f"执行时间：每天 {schedule_time}")
    print(f"按 Ctrl+C 停止\n")

    # 设置每日定时任务
    schedule.every().day.at(schedule_time).do(daily_task)

    # 持续运行
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "now":
        # 立即执行一次
        print("立即执行任务...")
        daily_task()
    else:
        # 启动定时调度器
        run_scheduler()
