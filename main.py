import logging
import os
import random
import urllib.request
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 杭州地标列表
LANDMARKS = [
    "西湖断桥",
    "雷峰塔",
    "三潭印月",
    "灵隐寺",
    "西溪湿地",
    "钱塘江大桥",
    "六和塔",
    "苏堤春晓",
    "平湖秋月",
    "曲院风荷",
    "花港观鱼",
    "柳浪闻莺",
    "南屏晚钟",
    "双峰插云",
    "宝石山",
    "湖滨步行街",
    "河坊街",
    "南宋御街",
    "京杭大运河",
    "拱宸桥",
]


def get_client():
    """初始化 OpenAI 客户端"""
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )


def query_weather(client, city, date_str):
    """查询城市天气"""
    logger.info(f"正在查询 {city} 的天气...")
    response = client.chat.completions.create(
        model="gemini-3-pro-preview",
        extra_body={"refresh_session": True},
        messages=[{
            "role": "user",
            "content": f"""请使用网络搜索功能，访问以下天气网站查询 {city} 现在的实时天气：
1. 中国天气网 (https://www.weather.com.cn)
2. 墨迹天气 (https://tianqi.moji.com)
3. 和风天气 (https://www.qweather.com)

注意：现在是{date_str}。

请务必通过搜索获取真实数据，不要猜测或编造。综合多个来源，只回复以下格式：

天气：[天气状况]
温度：[当前温度]℃
最高/最低：[最高]℃/[最低]℃
湿度：[湿度]%
风：[风向][风力]
"""
        }],
        stream=False
    )
    weather_info = response.choices[0].message.content
    logger.info(f"天气查询结果：\n{weather_info}")
    return weather_info


def generate_image(client, city, date_str, date_time, landmark, weather_info):
    """根据天气生成图片"""
    logger.info(f"正在生成 {city} 天气图片（地标：{landmark}）...")

    image_prompt = f"""
【{city}，{date_str}】

【真实天气数据】
{weather_info}

请根据以上真实天气数据生成图片。

【风格】
– 所有元素（建筑物、树木、车辆、人物、地标、标志等）均以钩针玩偶的形式呈现。
– 人物也以可爱的钩针玩偶形式出现，表情萌趣，四肢短小，比例圆润。
– 柔和的粉彩色调 + 舒适的针织纹理。
– 背景是一个完全由针织元素构成的微缩城市世界。

【天气表现】
– 根据上面的真实天气数据准确反映天气状况：

降水表现：
• 小雨/毛毛雨 → 稀疏的毛线细雨丝，淡淡的湿润色调
• 中雨 → 密集的毛线雨滴，地面有小水洼
• 大雨/暴雨 → 粗重的毛线雨帘，飞溅的针织水花，深灰色背景
• 小雪 → 零星的钩针小雪花轻轻飘落
• 中雪 → 密集的钩针雪花，地面薄雪层
• 大雪/暴雪 → 漫天飞舞的大片钩针雪花，厚厚的针织积雪
• 雨夹雪 → 毛线雨滴与钩针雪花交织

天空表现：
• 晴朗 → 柔和的粉彩蓝天，毛绒太阳
• 多云 → 蓬松的针织白云点缀天空
• 阴天 → 厚重的灰色针织云层覆盖
• 雾/霾 → 朦胧的毛毡雾气弥漫

风力表现：
• 微风(1-2级) → 树叶和旗帜轻轻摆动
• 和风(3-4级) → 树枝明显摇晃，毛线飘带飞扬
• 大风(5-6级) → 树木大幅摆动，云朵快速移动，人物围巾飘起
• 强风(7级以上) → 树木剧烈弯曲，落叶纷飞，画面动感强烈

[自动时区反映]
- 当前时间是{date_time} 不用展示！只是作为背景氛围依据！
– 背景氛围会根据当前时间而变化：
• 早晨 (06:00-11:00) → 柔和的粉彩天空，晨光温柔
• 中午 (11:00-14:00) → 明亮的阳光，色彩鲜明
• 下午 (14:00-17:00) → 温暖的光线，金色调
• 日落 (17:00-19:00) → 橙粉色的针织日落，晚霞绚丽
• 傍晚 (19:00-21:00) → 针织玩偶夜景，点缀着小巧的针织灯，天空渐暗
• 夜晚 (21:00-06:00) → 深蓝色的针织天空 + 毛毡星星，宁静夜色

[背景构成]
– 以针织玩偶的形式重新诠释具有代表性的城市地标：{landmark}，要完整显示！
– 并在左下角显示地标名称
– 自动生成中文标识，使其以钩针编织的风格自然呈现。

[界面布局]
– 顶部中央显示城市名称
– 下方显示日期
– 下方显示今日实际温度范围（使用真实天气数据中的温度）
– 今日天气图标（云/晴/雪/雨等，由毛线制成）
– 底部无文字。

[自动文本颜色优化]
文本颜色会根据背景亮度、色调、天气状况和时间自动调整，以提高可读性。

[整体色调]
– 9:16 比例
– 温馨的冬日氛围，柔和的光线
– 一个可爱、简洁的微缩世界
"""

    response = client.chat.completions.create(
        model="gemini-3-pro-preview",
        extra_body={"refresh_session": True},
        messages=[{"role": "user", "content": image_prompt}],
        stream=False
    )

    return response


def download_image(response, city):
    """下载生成的图片，返回文件路径"""
    os.makedirs("generated_images", exist_ok=True)

    raw = response.model_dump()
    content = raw["choices"][0]["message"]["content"]

    if isinstance(content, list):
        for item in content:
            if item.get("type") == "image_url":
                url = item["image_url"]["url"]
                logger.info(f"图片 URL：{url}")

                file_date = datetime.now().strftime("%Y%m%d_%H%M")
                file_path = f"generated_images/{city}_{file_date}.png"

                urllib.request.urlretrieve(url, file_path)
                logger.info(f"图片已保存：{file_path}")
                return file_path
    else:
        logger.warning(f"响应内容：{content}")
        return None


def generate_weather_image(city="杭州市"):
    """
    生成天气图片的主函数

    Args:
        city: 城市名称

    Returns:
        tuple: (图片路径, 天气信息, 地标名称) 或 (None, None, None) 如果失败
    """
    try:
        # 初始化
        client = get_client()
        date_str = datetime.now().strftime("%Y.%m.%d")
        date_time = datetime.now().strftime("%H:%M")
        landmark = random.choice(LANDMARKS)

        logger.info(f"本次选中地标：{landmark}")

        # 查询天气
        weather_info = query_weather(client, city, date_str)

        # 生成图片
        response = generate_image(client, city, date_str, date_time, landmark, weather_info)

        # 下载图片
        image_path = download_image(response, city)

        return image_path, weather_info, landmark

    except Exception as e:
        logger.error(f"生成图片失败：{e}")
        return None, None, None


# 直接运行时执行
if __name__ == "__main__":
    # 单独运行时配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    image_path, weather_info, landmark = generate_weather_image()
    if image_path:
        logger.info(f"生成完成！图片路径：{image_path}")
