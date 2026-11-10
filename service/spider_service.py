from spider.china_weather_spider import weather_china
from spider.city_weather_spider import weather_city
from spider.history_weather_spider import weather_history

"""
爬虫相关接口调用服务层
"""


# 启动中国地区数据实时天气爬虫
def start_china_spider():
    weather_china()


# 启动西安地区数据实时天气爬虫
def start_city_spider():
    weather_city()


# 启动西安地区数据历史天气爬虫
def start_history_spider():
    weather_history()


def main_spider():
    weather_china()
    weather_city()
