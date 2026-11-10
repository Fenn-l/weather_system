from entity.model import HistoryWeather
from utils.JsonUtils import get_class_one, get_class_list
from utils.PageUtils import get_page_start, PageData
from utils.Result import Result
from utils.SySQL import SQLManager

"""
<西安>历史气象数据相关业务逻辑服务层
"""


# 根据ID从数据库中查询历史天气数据
def select_history_weather_by_id(id):
    sql = "SELECT * FROM historyweather WHERE id=%s"
    sqlManager = SQLManager()
    data = sqlManager.get_one(sql, id)
    history_weather = get_class_one(data, HistoryWeather)
    sqlManager.close()
    return history_weather

# 根据分页参数和查询条件，从数据库中获取历史天气数据的分页结果
def select_history_weather_list(page, limit, where):
    page, limit, where = get_page_start(int(page), int(limit), where)
    params_sql = get_search_params(where)
    data_sql = "SELECT * FROM historyweather WHERE 1=1 " + params_sql + " ORDER BY id DESC LIMIT %s,%s"
    count_sql = "SELECT COUNT(id) as i FROM HistoryWeather WHERE 1=1 " + params_sql
    sqlManager = SQLManager()
    data = sqlManager.get_list(data_sql, (page, limit))  # 获取分页数据
    count = sqlManager.get_one(count_sql)['i']  # 获取数据总数
    history_weather = get_class_list(data, HistoryWeather)
    page_result = PageData(count, history_weather)
    return page_result


# 据输入的where字典生成SQL查询条件字符串
def get_search_params(where):
    sql = ''
    if where:
        if where['cityname'] and len(where['cityname']) > 0:
            sql = sql + " AND cityname like '%%" + where['cityname'] + "%%' "
        if where['record_date'] and len(where['record_date']) > 0:
            sql = sql + " AND record_date = '" + where['record_date'] + "' "
    return sql


# 从数据库中获取所有不同的天气类型
def get_weather_list():
    sql = "select weather from historyweather group by weather"
    sqlManager = SQLManager()
    weather_list = []
    data = sqlManager.get_list(sql)
    for i in data:
        weather_list.append(i['weather'])
    sqlManager.close()
    return weather_list


# 从数据库表 historyweather 中获取风向 (wd) 列表
def get_wd_list():
    sql = "select wd from historyweather group by wd"
    sqlManager = SQLManager()
    wd_list = []
    data = sqlManager.get_list(sql)
    for i in data:
        wd_list.append(i['wd'])
    sqlManager.close()
    return wd_list


# 从数据库中获取城市名称列表
def get_city_list():
    sql = "select cityname from historyweather group by cityname"
    sqlManager = SQLManager()
    city_list = []
    data = sqlManager.get_list(sql)
    for i in data:
        city_list.append(i['cityname'])
    sqlManager.close()
    return city_list


# 插入天气数据
def insert_history_weather(data):
    sqlManager = SQLManager()
    check_sql = "select count(id) as `i` from `historyweather` where cityname=%s and record_date= %s"
    count = sqlManager.get_one(check_sql, (data['cityname'], data['record_date']))['i']
    if count > 0:
        return Result(False, "数据重复")
    sql = "INSERT INTO historyweather (cityname,record_date,high,low,weather,wd,ws) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    sqlManager.instert(sql, (
        data['cityname'], data['record_date'], data['high'], data['low'], data['weather'], data['wd'], data['ws']))
    sqlManager.close()
    return Result(True, "添加成功")


# 修改天气
def edit_history_weather(data):
    sqlManager = SQLManager()
    sql = "update historyweather SET high=%s,low=%s,weather=%s,wd=%s,ws=%s where id=%s"
    sqlManager.moddify(sql, ( data['high'], data['low'], data['weather'], data['wd'], data['ws'], data['id']))
    sqlManager.close()
    return Result(True, "修改成功")


#
def del_history_weather(id):
    sqlManager = SQLManager()
    sql = "DELETE FROM historyweather where id=%s"
    sqlManager.moddify(sql, id)
    sqlManager.close()
    return Result(True, "删除成功")


#
def del_history_weather_list(ids):
    sqlManager = SQLManager()
    sql = "DELETE FROM historyweather where id in (" + ids + ")"
    sqlManager.moddify(sql)
    sqlManager.close()
    return Result(True, "删除成功")


def get_history_weather(id):
    sqlManager = SQLManager()
    sql = "select * from `historyweather` where id=%s "
    data = sqlManager.get_one(sql, id)
    sqlManager.close()
    return data
