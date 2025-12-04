"""测试完整流程：生成图片 + 发送邮件"""
from dotenv import load_dotenv
from scheduler import daily_task

# 加载环境变量
load_dotenv()

if __name__ == "__main__":
    print("测试完整流程（生成图片 + 发送邮件）")
    print("这可能需要几分钟时间...\n")
    daily_task()
