# 安装的库
import execjs
import requests
import json
# 内置库
import os
import datetime
from utils.SySQL import SQLManager
from utils.JsonUtils import read_json
from bs4 import BeautifulSoup
import time
from time import sleep
import random

# 获取

def getTheMounth(n):
    date=datetime.date.today()
    month=date.month
    month=4
    year=date.year
    year=2025
    for i in range(n):
        if month==1:
            year-=1
            month=12
        else:
            month-=1
    return datetime.date(year,month,1).strftime('%Y%m')

def weather_history(month_num=2):
    sqlManager = SQLManager()
    current_path=os.path.dirname(os.path.abspath(__file__)) # 获取当前文件所在的目录
    citys=read_json(os.path.join(current_path+'/city_pingyin.json'))
    count=0
    for city,pingyin in citys.items():
        print("[INFO]"+city+"历史气象数据爬虫启动，时间【最近"+str(month_num)+"月】")
        urls_before = ["https://lishi.tianqi.com/"+pingyin+"/" + getTheMounth(i) + ".html" for i in range(month_num)] # 前十天urls地址
        urls_after = ["http://lishi.tianqi.com/monthdata/"+pingyin+"/"+getTheMounth(i) for i in range(month_num) ] # 后十天urls
        headers_before = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "UserId=17403110452472343; Hm_lvt_7c50c7060f1f743bccf8c150a646e90a=1740311045; HMACCOUNT=3CB3518BE71D9B9E; UserId=17403112448745520; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1740311246; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1740311429; Hm_lpvt_7c50c7060f1f743bccf8c150a646e90a=1740311925",
            "Host": "lishi.tianqi.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }
        headers_after = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9",
            "connection": "keep-alive",
            "content-length": "55",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "UserId=17403110452472343; UserId=17403112448745520; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1740311246; Hm_lvt_7c50c7060f1f743bccf8c150a646e90a=1740311045,1740397226; HMACCOUNT=3CB3518BE71D9B9E; Hm_lpvt_7c50c7060f1f743bccf8c150a646e90a=1740403259",
            "host": "lishi.tianqi.com",
            "origin": "http://lishi.tianqi.com",
            "referer": "http://lishi.tianqi.com/xian/201805.html",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        for url1,url2 in zip (urls_before,urls_after):
            # 获取前十天
            backInfo = requests.get(url=url1, headers=headers_before)
            backInfo.encoding = 'utf-8'
            soup = BeautifulSoup(backInfo.content, 'html.parser')
            weather_list = soup.find("ul", class_="thrui")
            li_list = weather_list.select("li")
            for li in li_list:
                divs = li.select("div")
                date = divs[0].get_text().split()[0]
                temp_high = divs[1].get_text().replace("℃", '')
                temp_low = divs[2].get_text().replace("℃", '')
                if temp_low==None:
                    continue
                weather = divs[3].get_text()
                wd = divs[4].get_text().split()[0]
                if "级" not in divs[4].get_text().split()[1]:
                    ws = str(-1000)
                else:
                    ws = divs[4].get_text().split()[1].replace("级", "")
                print(city,city,date,temp_high,temp_low,weather,wd,ws)
                select_sql="select count(id) as `i` from `historyweather` where cityname='"+ city +"' and record_date='"+date +"'"
                insert_history_sql = "insert into `historyweather` values (NULL,'西安','" + city + "','" + date + "','" + str(temp_high) + "','" + str(temp_low) + "','" + weather + "','" + wd + "','" + str(ws) + "','" + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + "')"
                if sqlManager.get_one(select_sql)["i"]==0:
                    sqlManager.moddify(insert_history_sql)
                    count+=1
            sleep(10)
            # 后20天的数据爬取
            current_path = os.path.dirname(os.path.abspath(__file__))
            # 读取js文件
            js_file = open(current_path + "\\weather.js", encoding="utf-8").read()
            # 编译js文件
            js_code = execjs.compile(js_file)
            # 获取加密
            crpyte = js_code.call("GetSign", pingyin)
            data = {"crypte": crpyte}
            response = requests.post(url=url2, headers=headers_after, data=data)
            time.sleep(10)
            if response.text==[]:
                continue
            response.encoding = 'utf-8'
            json_data = response.json()
            for info in json_data:
                date = info["date_str"]
                temp_high = info["htemp"]
                if temp_high==None:
                    continue
                temp_low = info["ltemp"]
                weather = info["weather"]
                wd = info["WD"]
                if wd=="暂无实况":
                    continue
                if "级" not in divs[4].get_text().split()[1]:
                    ws = str(-1000)
                else:
                    ws = divs[4].get_text().split()[1].replace("级", "")

                print(city,city,date,temp_high,temp_low,weather,wd,ws)
                select_sql = "select count(id) as `i` from `historyweather` where cityname='" + city + "' and record_date='" + date + "'"
                insert_history_sql = "insert into `historyweather` values (NULL,'西安','" + city + "','" + date + "'," + str(
                    temp_high) + "," + str(temp_low) + ",'" + weather + "','" + wd + "','" + str(ws) + "','" + time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime()) + "')"

                if sqlManager.get_one(select_sql)["i"] == 0:
                    sqlManager.moddify(insert_history_sql)
                    count += 1
            sleep(10)
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 将数字转化成字符串
        sql = "insert into slog values(null,\"【爬虫运行】" + city + "历史气象数据爬虫爬取数据:" + str(
            count) + "条\",\"" + t + "\")"
        sqlManager.moddify(sql)
        print("[INFO]" + city + "历史气象数据爬虫完成，时间【最近" + str(month_num) + "月】")
    sqlManager.close()

# {'_id': '101110101_20250131', 'WD': '东风', 'WS': '2级', 'aqi': 230, 'date': '01/31', 'htemp': 9, 'img_num': '7', 'ltemp': 2, 'pm25': 180, 'weather': '小雨', 'week': '星期五', 'max_htemp': '17', 'min_ltemp': '-28', 'dates': '0131', 'date_str': '2025-01-31'}

if __name__ == '__main__':
    # 24
    weather_history(2)
