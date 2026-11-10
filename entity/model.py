# 全国气象数据
class CurrentWeather:
    def __int__(self, id, cityname, record_date, record_time, temp, wd, ws, wse, sd, weather, aqi, create_time, is_old):
        self.id = id
        self.cityname = cityname
        self.record_date = record_date
        self.record_time = record_time
        self.temp = temp
        self.wd = wd
        self.ws = ws
        self.wse = wse
        self.sd = sd
        self.weather = weather
        self.aqi = aqi
        self.create_time = create_time
        self.is_old = is_old


# 上海气象数据
class DetailWeather:
    def __int__(self, id, cityname, record_date, record_time, temp, wd, ws, wse, sd, weather, aqi, create_time, is_old):
        self.id = id
        self.cityname = cityname
        self.record_date = record_date
        self.record_time = record_time
        self.temp = temp
        self.wd = wd
        self.ws = ws
        self.wse = wse
        self.sd = sd
        self.weather = weather
        self.aqi = aqi
        self.create_time = create_time
        self.is_old = is_old


# 上海气象数据
class HistoryWeather:
    def __int__(self, id, nameen, cityname, record_date, high, low, weather, wd, ws, create_time):
        self.id = id
        self.nameen = nameen
        self.cityname = cityname
        self.record_date = record_date
        self.high = high
        self.low = low
        self.weather = weather
        self.wd = wd
        self.ws = ws
        self.create_time = create_time


# 系统用户数据
class User:
    def __int__(self, id, name, account, password, company, mail, type, status):
        self.id = id
        self.name = name
        self.account = account
        self.password = password
        self.company = company
        self.mail = mail
        self.type = type
        self.status = status


# 城市数据
class City:
    def __int__(self, id, city_name, city_code, city_py):
        self.id = id
        self.city_name = city_name
        self.city_code = city_code
        self.city_py = city_py


# 公告数据
class Notice:
    def __int__(self, id, title, content, user_name, create_time):
        self.id = id
        self.title = title
        self.content = content
        self.user_name = user_name
        self.create_time = create_time


# 日志数据
class Slog:
    def __int__(self, id, log, create_time):
        self.id = id
        self.log = log
        self.create_time = create_time
