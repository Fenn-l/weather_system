# 安装的库
import requests
import json
# 内置库
import os
import datetime
from utils.SySQL import SQLManager
from bs4 import BeautifulSoup
import time
# 自己写的库
from utils.JsonUtils import read_json # 自己写的read_json是JsonUtils.Py中的方法


class GetWeather:
    def __init__(self):
        self.baseUrl='http://getweather.api.bdymkt.com/lundear/weather1d'
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'X-Bce-Signature': 'AppCode/3aff14ce2d4d4ce3a1b5bdae04d83012'
        }
        self.cityDict={}
        current_path = os.path.dirname(os.path.abspath(__file__))
        # print(current_path)
        self.cityDict=read_json(current_path+"\china.json")
        self.category=read_json(current_path+"\category.json")


    def __getWeatherInfo__(self):
        sqlManager = SQLManager()# 创建对象
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        count=0
        for city,id in self.cityDict.items():
             # 统计爬取多少城市
            try:
                # 创建字典
                params = {}
                # 添加键值对
                params['areaCn'] = ''
                params['areaCode'] = id
                params['ip'] = ''
                params['lat'] = ''
                params['lng'] = ''
                params['need3hour'] = ''
                params['needIndex'] = ''
                params['needObserve'] = ''
                params['needalarm'] = ''
                params['need1hour'] = ''
                response = requests.get(url=self.baseUrl,params=params,headers=self.headers,allow_redirects=False)
                response.encoding = 'utf-8'
                self.htmlResult = response.text

                # print("1------",self.htmlResult)
                # print("2------",type(self.htmlResult))
                d=json.loads(self.htmlResult)
                date=d['data']

                nameen=date["cityInfo"]["areaEn"]  # 城市拼音
                cityname=city                       # 城市名称
                # 构造sql查询语句，用于查询城市名称和城市拼音是否存在
                judge_sql = "select count(id) as 'i' from citys where city_name= '" +  cityname  + "' and city_py='" + nameen +"'"
                # 执行sql语句并获得结果 i 字段的值
                i=sqlManager.get_one(judge_sql)['i']
                # 如果城市信息在citys中不存在
                if i==0:
                    # 构造插入语句，用于添加新的城市信息到数据库
                    city_insert_sql = "insert into citys values (NULL,'" + cityname + "','" + id + "','" + nameen + "')"
                    # 执行sql语句，添加城市信息
                    sqlManager.moddify(city_insert_sql)

                temp=date["now"]["temp"]    # 当前温度
                WD=date["now"]["WD"]                # 风向
                WS=date["now"]["WS"].replace("级","")               # 风力
                wse=date["now"]["wse"].replace("km/h","")           # 风速
                sd=date["now"]["SD"].replace("%","")                # 湿度
                weather= date["now"]["weather"]      # 天气
                record_date=today  # 时间
                record_time=date["now"]["time"]     # 时分
                rain24h=date["now"]["rain24h"]      # 24h降雨量
                aqi=date["now"]["aqi"]              # 空气质量
                print("[INFO] 正在处理数据:",date)

                judge_sql="select count(id) as `i` from `currentweather` where cityname='" + cityname + "' and record_date='" + record_date + "' and record_time='" + record_time + "'"
                i=sqlManager.get_one(judge_sql)['i']
                if int(i)>0:
                    continue
                update_sql = "update `currentweather` set is_old = 1  where cityname='" + cityname + "'"  # 更新旧数据
                sqlManager.moddify(update_sql)
                sql="INSERT INTO `currentweather` VALUES (null, '" + self.category[cityname] + "', '" + cityname + "', '" + record_date + "', '" + record_time + "', " + str(temp) + ", '" + WD + "', " + WS + ", " + wse + ", " + sd + ", '" + weather + "', " + rain24h + "," + aqi + ", '" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "',0);"
                sqlManager.moddify(sql)
                count+=1
            except Exception as e:
                print(e)
                # continue

        t=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 将数字转化成字符串
        sql="insert into slog values(null,\"【爬虫启动】获取全国气象数据成功，获取数据:"+str(count)+"条\",\""+t+"\")"
        sqlManager.moddify(sql)
        sqlManager.close()

    def __main__(self):
        print("[INFO]全国实时气象数据爬虫启动，时间【"+str(datetime.datetime.now())+"】")
        self.__getWeatherInfo__()
        print("[INFO]全国实时气象数据爬虫完成，时间【"+str(datetime.datetime.now())+"】")

def weather_china():
    weather=GetWeather()
    weather.__main__()

if __name__ == '__main__':
    weather_china()

