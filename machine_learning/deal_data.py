import json
import time
import os

module_path = os.path.dirname(__file__)

import pandas as pd

city_dict = {}
city_list = []
city_no_dict = {}
city_file = module_path + "/city_category.json"
# 打开一个文件用于读取JSON数据
if os.path.getsize(city_file) == 0:
    print(city_file, "文件为空")
else:
    with open(city_file, 'r') as file:
        city_dict = json.load(file)
    for i in city_dict:
        city_no_dict[city_dict[i]] = i
        city_list.append(i)
weather_dict = {}
weather_list = []
weather_no_dict = {}
weather_file = module_path + "/weather_category.json"
# 打开一个文件用于读取JSON数据
if os.path.getsize(weather_file) == 0:
    print(weather_file, "文件为空")
else:
    with open(weather_file, 'r') as file:
        weather_dict = json.load(file)
    for i in weather_dict:
        weather_no_dict[weather_dict[i]] = i
        weather_list.append(i)

wd_no_dict = {}
wd_dict = {}
wd_dict_list = []
wd_file = module_path + "/wd_category.json"
# 打开一个文件用于读取JSON数据
if os.path.getsize(wd_file) == 0:
    print(wd_file, "文件为空")
else:
    with open(wd_file, 'r') as file:
        wd_dict = json.load(file)
    for i in wd_dict:
        wd_no_dict[wd_dict[i]] = i
        wd_dict_list.append(i)


# 格式化全部数据
def transformer_data(path='./output_file_modified.csv'):
    city_no = -1
    next_data = []
    all_data = []
    history_data = pd.read_csv(path)
    for province, cityname, record_date, high, low, weather, wd, ws  in history_data.values:
        cityname, record_date, high, low, weather, wd, ws = transformer_item(cityname, record_date, high, low, weather,
                                                                             wd, ws)

        itmes = [cityname, record_date, high, low, weather, wd, ws]
        if city_no != cityname:
            next_data = [cityname, record_date, high, low, weather, wd, ws]
            city_no = cityname
            continue
        else:
            next_data.extend(itmes)
            all_data.append(next_data)
            next_data = itmes
    import json
    # 打开一个文件用于写入JSON数据
    with open(weather_file, 'w') as file:
        json.dump(weather_dict, file)
    # 打开一个文件用于写入JSON数据
    with open(wd_file, 'w') as file:
        json.dump(wd_dict, file)
    # 打开一个文件用于写入JSON数据
    with open(city_file, 'w') as file:
        json.dump(city_dict, file)
    return all_data


# 格式化独立行数据
# ①序列化城市
# ②日期时间戳
# ③序列化天气
# ④序列化风向
def transformer_item(cityname, record_date, high, low, weather, wd, ws):
    timeArray = time.strptime(str(record_date), "%Y-%m-%d")
    record_date = int(time.mktime(timeArray))
    if weather not in weather_list:
        weather_dict[weather] = len(weather_list)
        weather_list.append(weather)
    if wd not in wd_dict_list:
        wd_dict[wd] = len(wd_dict_list)
        wd_dict_list.append(wd)
    if cityname not in city_list:
        city_dict[cityname] = len(city_list)
        city_list.append(cityname)
    return city_dict[cityname], record_date, high, low, weather_dict[weather], wd_dict[wd], ws  # 格式化独立行数据


# ③反序列化天气
# ④反序列化风向
def de_transformer_item(city, record_date, high, low, weather, wd, ws):
    return city, record_date.strftime("%Y-%m-%d"), round(high), round(low), weather_no_dict[round(weather)], wd_no_dict[
        round(wd)], round(ws)


import datetime


# 获取未来几天的时间戳
def getNextDay(day=1):
    today = datetime.date.today()
    oneday = datetime.timedelta(days=day)
    day_time = today + oneday
    return int(time.mktime(day_time.timetuple())), day_time


if __name__ == '__main__':
    transformer_data()
    #print(transformer_item("闵行", "2023-01-01", 34, 28, "阴", "东南风", 2))
