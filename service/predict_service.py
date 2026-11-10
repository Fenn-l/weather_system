from entity.model import DetailWeather
from machine_learning import model_predict
from utils.JsonUtils import get_class_one

from utils.SySQL import SQLManager


def predict(cityname="西安"):
    sql = "SELECT * FROM detailweather WHERE cityname=%s order by id desc limit 1"
    sql_max = "SELECT max(temp) as i FROM detailweather group by record_date having record_date=%s"
    sql_min = "SELECT min(temp) as i FROM detailweather group by record_date having record_date=%s"
    sqlManager = SQLManager()
    data = sqlManager.get_one(sql, cityname)
    detail_weather = get_class_one(data, DetailWeather)
    max = sqlManager.get_one(sql_max, detail_weather.record_date)["i"]
    min = sqlManager.get_one(sql_min, detail_weather.record_date)["i"]
    result = model_predict.predict(cityname, detail_weather.record_date, max, min, detail_weather.weather,
                                   detail_weather.wd,
                                   detail_weather.ws)
    sqlManager.close()
    weather_list = []
    days = []
    t1 = []
    t2 = []
    for city, date, high, low, weather, wd, ws in result:
        weather_list.append({"day": date, "weather": weather})
        days.append(date)
        t1.append(high)
        t2.append(low)
    return {"weather_list": weather_list, "days": days, "t1": t1, "t2": t2}
