"""测试邮件发送功能"""
import os
from dotenv import load_dotenv
from scheduler import send_email

# 加载环境变量
load_dotenv()

def test_email():
    """测试邮件发送（不生成图片）"""
    print("=" * 50)
    print("测试邮件发送功能")
    print("=" * 50)

    city = os.getenv("CITY", "杭州市")

    # 模拟数据
    test_weather = """天气：晴
温度：12℃
最高/最低：15℃/8℃
湿度：65%
风：东北风2级"""
    test_landmark = "西湖断桥（测试）"

    print(f"城市：{city}")
    print(f"地标：{test_landmark}")
    print(f"天气：\n{test_weather}")
    print()

    # 发送测试邮件（无图片附件）
    success = send_email(None, test_weather, test_landmark, city)

    print()
    if success:
        print("✅ 邮件测试成功！配置正确")
    else:
        print("❌ 邮件测试失败！请检查 .env 配置")

    return success


if __name__ == "__main__":
    test_email()
