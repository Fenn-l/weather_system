from entity.model import CurrentWeather
from utils.JsonUtils import get_class_list
from utils.SySQL import SQLManager


# 气象分类
# 根据指定的城市名称，统计该城市的历史天气类型及其出现次数
def weather_category_data(city):
    sqlManager = SQLManager()
    key_sql = "select weather from historyweather where cityname ='" + city + "' group by weather"
    value_sql = "select count(id) as `value`,weather as `name` from historyweather where cityname ='" + city + "' group by weather"
    key_data = sqlManager.get_list(key_sql)
    # print(key_data,"----1-----")
    value_data = sqlManager.get_list(value_sql)
    # print(value_data,"-----2-----")
    x_data = [k['weather'] for k in key_data]
    sqlManager.close()
    return {'x': x_data, 'y': value_data}


# 根据指定城市名称，统计历史天气数据中不同风向的分布情况
def wd_category_data(city):
    sqlManager = SQLManager()
    key_sql = "select wd from historyweather where cityname ='" + city + "' group by wd"
    value_sql = "select count(id) as `value`,wd as `name` from historyweather where cityname ='" + city + "'  group by wd"
    key_data = sqlManager.get_list(key_sql)
    value_data = sqlManager.get_list(value_sql)
    x_data = [k['wd'] for k in key_data]
    sqlManager.close()
    return {'x': x_data, 'y': value_data}


# 根据指定城市名称，从历史天气数据中统计风速等级的分布情况
def ws_category_data(city):
    sqlManager = SQLManager()
    key_sql = "select ws from historyweather where cityname ='" + city + "'  group by ws"
    value_sql = "select count(id) as `value`,ws as `name` from historyweather where cityname ='" + city + "'  group by ws"
    key_data = sqlManager.get_list(key_sql)
    value_data = sqlManager.get_list(value_sql)
    x_data = [str(k['ws']) + '级' for k in key_data]
    y_data = [{'value': i['value'], 'name': str(i['name']) + '级'} for i in value_data]
    sqlManager.close()
    return {'x': x_data, 'y': y_data}


# 根据城市名称从数据库中获取最近15天的天气记录，并返回日期、最高温度和最低温度的数据列表
def temp_data(city):
    sqlManager = SQLManager()
    data_sql = "select record_date,high,low from historyweather where cityname ='" + city + "'  order by record_date desc limit 15"
    data = sqlManager.get_list(data_sql)
    x_data = [k['record_date'] for k in data]
    y1_data = [k['high'] for k in data]
    y2_data = [k['low'] for k in data]
    x_data.reverse()
    y1_data.reverse()
    y2_data.reverse()
    sqlManager.close()
    return {'x': x_data, 'y1': y1_data, 'y2': y2_data}


# 根据指定的城市名称，从数据库表currentweather中查询最近15条气象记录，并返回包含时间、温度、空气质量指数(AQI)、风速(wse)和降雨量(rain)等信息
def current_change_data(city):
    sqlManager = SQLManager()
    data_sql = "select record_date,record_time,temp,aqi,wse,rain from currentweather where cityname ='" + city + "'  order by record_date desc limit 15"
    data = sqlManager.get_list(data_sql)
    x_data = [str(k['record_date']) + ' ' + str(k['record_time']) for k in data]
    temp_data = [k['temp'] for k in data]
    aqi_data = [k['aqi'] for k in data]
    wse_data = [k['wse'] for k in data]
    rain_data = [k['rain'] for k in data]
    x_data.reverse()
    temp_data.reverse()
    aqi_data.reverse()
    wse_data.reverse()
    rain_data.reverse()
    return {'x': x_data, 'temp_data': temp_data, 'aqi_data': aqi_data, 'wse_data': wse_data, 'rain_data': rain_data}


# 获取首页需要展示的气象数据
def top_page_data():
    sqlManager = SQLManager()
    key_sql = "select weather,count(id) as n from currentweather where is_old=0  group by weather order by count(id) desc limit 4"
    key_data = sqlManager.get_list(key_sql)
    num_data = [{k['weather']: k['n']} for k in key_data]
    table_sql = "select * from currentweather where cityname in ('北京','上海','广州','深圳','南京','杭州','青岛','苏州','武汉','郑州') and is_old=0"
    table_data = sqlManager.get_list(table_sql)
    # table_list = get_class_list(table_data,CurrentWeather)
    temp_top_sql = "select cityname,temp from currentweather where is_old=0 order by temp desc limit 15"
    temp_list = sqlManager.get_list(temp_top_sql)
    temp_data = [{'city': i['cityname'], '温度': i['temp'], } for i in temp_list]
    rain_top_sql = "select cityname,rain from currentweather where is_old=0 order by rain desc limit 15"
    rain_list = sqlManager.get_list(rain_top_sql)
    rain_data = [{'city': i['cityname'], '降雨量': float(i['rain']), } for i in rain_list]
    aqi_top_sql = "select cityname,aqi from currentweather where is_old=0 order by aqi desc limit 15"
    aqi_list = sqlManager.get_list(aqi_top_sql)
    aqi_data = [{'city': i['cityname'], 'AQI': i['aqi'], } for i in aqi_list]
    sqlManager.close()
    return {'num_data': num_data, 'table_data': table_data, 'aqi_data': aqi_data, 'rain_data': rain_data,
            'temp_data': temp_data}


# if __name__ == '__main__':
#     print(weather_category_data("西安"))