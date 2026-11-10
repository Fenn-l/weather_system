import datetime

from flask import Flask as _Flask, flash, redirect
from flask import request, session
from flask import render_template
from flask.json import JSONEncoder as _JSONEncoder, jsonify
import decimal
import os

from flask_apscheduler import APScheduler

from service import user_service, current_weather_service, detail_weather_service, history_weather_service, \
    spider_service, city_service, notice_service, slog_service, data_service, predict_service

from utils.JsonUtils import read_json
import datetime

from utils.Result import Result

base = os.path.dirname(__file__)
directory_path = os.path.dirname(__file__)
json_path = directory_path + '/static/api/'


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        super(_JSONEncoder, self).default(o)


class Flask(_Flask):
    json_encoder = JSONEncoder


import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)


# ----------------------------------------------页面加载模块开始----------------------------------------------
# 加载系统json文件
@app.route('/api/<string:path>/')
def api_json(path):
    if path == 'init.json' and session.get('user') and session.get('user')['type'] == 1:
        path = 'custom_init.json'
    return read_json(json_path + path)


# 加载page下的静态页面
@app.route('/page/<string:path>')
def api_path(path):
    return render_template("page/" + path)


# 系统默认路径后台跳转
@app.route('/admin')
def admin_page():
    if session.get('user') and session.get('user')['id'] > 0:
        return render_template("index.html")
    else:
        return redirect("/login")


# 系统默认路径前台跳转
@app.route('/')
def main_page():
    return render_template("page/login.html")


# 系统登录路径
@app.route('/login')
def login_page():
    return render_template("page/login.html")


# 系统退出登录路径
@app.route('/logout')
def logout_page():
    session.clear()
    return redirect("/login")


# 系统注册用户
@app.route('/register', methods=['get'])
def register_page():
    return render_template("page/register.html")


# ----------------------------------------------页面加载模块结束----------------------------------------------


# ----------------------------------------------用户相关模块开始----------------------------------------------
# 用户注册
@app.route('/register', methods=['post'])
def register_user():
    form = request.form.to_dict()  # 获取值
    result = user_service.insert_user(form)
    return result.get()


# 用户登录
@app.route('/login', methods=['post'])
def login_user():
    form = request.form.to_dict()  # 获取值
    result = user_service.select_user_by_account_password(form)
    session['user'] = result.data
    return result.get()


# ----------------------------------------------用户相关模块结束----------------------------------------------

# ----------------------------------------------全国气象相关模块开始----------------------------------------------
# 全国气象数据分页
@app.route('/page/current/weather/add', methods=['get'])
def page_current_weather_add():
    city_list = current_weather_service.get_city_list()
    wd_list = current_weather_service.get_wd_list()
    weather_list = current_weather_service.get_weather_list()
    return render_template("page/currentWeather/add.html", city_list=city_list, weather_list=weather_list,
                           wd_list=wd_list)


# 添加全国气象数据
@app.route('/add/current/weather', methods=['post'])
def add_current_weather():
    form = request.form.to_dict()
    result = current_weather_service.insert_current_weather(form)
    return result.get()


# 全国气象数据编辑页面
@app.route('/page/current/weather/edit', methods=['get'])
def page_current_weather_edit():
    id = request.args.get('id')
    current_weather = current_weather_service.get_current_weather(id)
    city_list = current_weather_service.get_city_list()
    wd_list = current_weather_service.get_wd_list()
    weather_list = current_weather_service.get_weather_list()
    return render_template("page/currentWeather/edit.html", city_list=city_list, weather_list=weather_list,
                           wd_list=wd_list, current_weather=current_weather)


# 编辑全国气象接口
@app.route('/edit/current/weather', methods=['post'])
def edit_current_weather():
    form = request.form.to_dict()
    result = current_weather_service.edit_current_weather(form)
    return result.get()


# 单个删除全国气象接口
@app.route('/del/current/weather/<int:id>', methods=['post'])
def del_current_weather(id):
    result = current_weather_service.del_current_weather(id)
    return result.get()


# 批量删除全国气象接口
@app.route('/del/current/weather', methods=['post'])
def del_current_weather_list():
    ids = request.args.get('ids')
    result = current_weather_service.del_current_weather_list(ids)
    return result.get()


# 全国气象数据分页
@app.route('/list/current/weather', methods=['get'])
def current_weather_list():
    page = request.args.get('page')
    limit = request.args.get('limit')
    where = request.args.get('searchParams')
    result = current_weather_service.select_current_weather_list(page, limit, where)
    return result.get()


# ----------------------------------------------全国气象相关模块结束----------------------------------------------


# ----------------------------------------------上海气象相关模块开始----------------------------------------------
# 西安气象数据分页
@app.route('/page/detail/weather/add', methods=['get'])
def page_detail_weather_add():
    city_list = detail_weather_service.get_city_list()
    wd_list = detail_weather_service.get_wd_list()
    weather_list = detail_weather_service.get_weather_list()
    return render_template("page/detailWeather/add.html", city_list=city_list, weather_list=weather_list,
                           wd_list=wd_list)


# 添加西安气象数据
@app.route('/add/detail/weather', methods=['post'])
def add_detail_weather():
    form = request.form.to_dict()
    result = detail_weather_service.insert_detail_weather(form)
    return result.get()


# 西安气象数据编辑页面
@app.route('/page/detail/weather/edit', methods=['get'])
def page_detail_weather_edit():
    id = request.args.get('id')
    detail_weather = detail_weather_service.get_detail_weather(id)
    city_list = detail_weather_service.get_city_list()
    wd_list = detail_weather_service.get_wd_list()
    weather_list = detail_weather_service.get_weather_list()
    return render_template("page/detailWeather/edit.html", city_list=city_list, weather_list=weather_list,
                           wd_list=wd_list, detail_weather=detail_weather)


# 编辑西安气象接口
@app.route('/edit/detail/weather', methods=['post'])
def edit_detail_weather():
    form = request.form.to_dict()
    result = detail_weather_service.edit_detail_weather(form)
    return result.get()


# 单个删除西安气象接口
@app.route('/del/detail/weather/<int:id>', methods=['post'])
def del_detail_weather(id):
    result = detail_weather_service.del_detail_weather(id)
    return result.get()


# 批量删除西安气象接口
@app.route('/del/detail/weather', methods=['post'])
def del_detail_weather_list():
    ids = request.args.get('ids')
    result = detail_weather_service.del_detail_weather_list(ids)
    return result.get()


# 西安气象数据分页
@app.route('/list/detail/weather', methods=['get'])
def detail_weather_list():
    page = request.args.get('page')
    limit = request.args.get('limit')
    where = request.args.get('searchParams')
    result = detail_weather_service.select_detail_weather_list(page, limit, where)
    return result.get()


# ----------------------------------------------上海气象相关模块结束----------------------------------------------

# ----------------------------------------------上海历史气象相关模块开始----------------------------------------------
# 西安历史数据分页
@app.route('/page/history/weather/add', methods=['get'])
def page_history_weather_add():
    city_list = history_weather_service.get_city_list()
    wd_list = history_weather_service.get_wd_list()
    weather_list = history_weather_service.get_weather_list()
    return render_template("page/historyWeather/add.html", city_list=city_list, weather_list=weather_list,
                           wd_list=wd_list)


# 添加西安历史数据
@app.route('/add/history/weather', methods=['post'])
def add_history_weather():
    form = request.form.to_dict()
    result = history_weather_service.insert_history_weather(form)
    return result.get()


# 西安历史编辑页面
@app.route('/page/history/weather/edit', methods=['get'])
def page_history_weather_edit():
    id = request.args.get('id')
    history_weather = history_weather_service.get_history_weather(id)
    city_list = history_weather_service.get_city_list()
    wd_list = history_weather_service.get_wd_list()
    weather_list = history_weather_service.get_weather_list()
    return render_template("page/historyWeather/edit.html", city_list=city_list, weather_list=weather_list,
                           wd_list=wd_list, history_weather=history_weather)


# 编辑西安历史接口
@app.route('/edit/history/weather', methods=['post'])
def edit_history_weather():
    form = request.form.to_dict()
    result = history_weather_service.edit_history_weather(form)
    return result.get()


# 单个删除西安历史接口
@app.route('/del/history/weather/<int:id>', methods=['post'])
def del_history_weather(id):
    result = history_weather_service.del_history_weather(id)
    return result.get()


# 批量删除西安历史接口
@app.route('/del/history/weather', methods=['post'])
def del_history_weather_list():
    ids = request.args.get('ids')
    result = history_weather_service.del_history_weather_list(ids)
    return result.get()


# 西安历史气象数据分页
@app.route('/list/history/weather', methods=['get'])
def history_weather_list():
    page = request.args.get('page')
    limit = request.args.get('limit')
    where = request.args.get('searchParams')
    result = history_weather_service.select_history_weather_list(page, limit, where)
    return result.get()


# ----------------------------------------------西安历史气象相关模块结束----------------------------------------------


# ----------------------------------------------用户相关模块开始----------------------------------------------
# 用户数据分页
@app.route('/page/user/add', methods=['get'])
def page_user_add():
    return render_template("page/user/add.html")


@app.route('/add/user', methods=['post'])
def add_user():
    form = request.form.to_dict()
    result = user_service.insert_user(form)
    return result.get()


# 用户修改密码
@app.route('/user/reset/password', methods=['post'])
def reset_password_user():
    form = request.form.to_dict()  # 获取值
    result = user_service.reset_password(form['old_password'], form['new_password'], form['again_password'])
    return result.get()


# 用户编辑页面
@app.route('/page/user/edit', methods=['get'])
def page_user_edit():
    id = request.args.get('id')
    user = user_service.get_user(id)
    return render_template("page/user/edit.html", user=user)


# 编辑用户接口
@app.route('/edit/user', methods=['post'])
def edit_user():
    form = request.form.to_dict()
    result = user_service.edit_user(form)
    return result.get()


# 单个删除用户接口
@app.route('/del/user/<int:id>', methods=['post'])
def del_user(id):
    result = user_service.del_user(id)
    return result.get()


# 批量删除用户接口
@app.route('/del/user', methods=['post'])
def del_user_list():
    ids = request.args.get('ids')
    result = user_service.del_user_list(ids)
    return result.get()


# 用户数据分页
@app.route('/list/user', methods=['get'])
def user_list():
    page = request.args.get('page')
    limit = request.args.get('limit')
    where = request.args.get('searchParams')
    result = user_service.select_user_list(page, limit, where)
    return result.get()


# ----------------------------------------------用户相关模块结束----------------------------------------------


# ----------------------------------------------公告相关模块开始----------------------------------------------
# 公告添加页面
@app.route('/page/notice/add', methods=['get'])
def page_notice_add():
    return render_template("page/notice/add.html")


@app.route('/add/notice', methods=['post'])
def add_notice():
    form = request.form.to_dict()
    result = notice_service.insert_notice(form)
    return result.get()


# 数据公告编辑页面
@app.route('/page/notice/edit', methods=['get'])
def page_notice_edit():
    id = request.args.get('id')
    notice = notice_service.get_notice(id)
    return render_template("page/notice/edit.html", notice=notice)


# 编辑公告接口
@app.route('/edit/notice', methods=['post'])
def edit_notice():
    form = request.form.to_dict()
    result = notice_service.edit_notice(form)
    return result.get()


# 单个删除公告接口
@app.route('/del/notice/<int:id>', methods=['post'])
def del_notice(id):
    result = notice_service.del_notice(id)
    return result.get()


# 批量删除公告接口
@app.route('/del/notice', methods=['post'])
def del_notice_list():
    ids = request.args.get('ids')
    result = notice_service.del_notice_list(ids)
    return result.get()


# 公告数据分页
@app.route('/list/notice', methods=['get'])
def notice_list():
    page = request.args.get('page')
    limit = request.args.get('limit')
    where = request.args.get('searchParams')
    result = notice_service.select_notice_list(page, limit, where)
    return result.get()


# 公告数据分页
@app.route('/get/notice/new', methods=['get'])
def get_new_notice():
    result = notice_service.get_notice_by_new()
    return result.get()


# ----------------------------------------------公告相关模块结束----------------------------------------------

# ----------------------------------------------日志相关模块开始----------------------------------------------

# 单个删除日志接口
@app.route('/del/slog/<int:id>', methods=['post'])
def del_slog(id):
    result = slog_service.del_slog(id)
    return result.get()


# 批量删除日志接口
@app.route('/del/slog', methods=['post'])
def del_slog_list():
    ids = request.args.get('ids')
    result = slog_service.del_slog_list(ids)
    return result.get()


# 日志数据分页
@app.route('/list/slog', methods=['get'])
def slog_list():
    page = request.args.get('page')
    limit = request.args.get('limit')
    where = request.args.get('searchParams')
    result = slog_service.select_slog_list(page, limit, where)
    return result.get()


# ----------------------------------------------日志相关模块结束----------------------------------------------


# ----------------------------------------------分析相关模块开始----------------------------------------------

# 西安城市数据分析
@app.route('/data/history/weather', methods=['post', 'get'])
def data_history_category():
    city = request.args.get('city')
    result_weather = data_service.weather_category_data(city)
    result_wd = data_service.wd_category_data(city)
    result_ws = data_service.ws_category_data(city)
    result_temp = data_service.temp_data(city)
    return {"weather_data": result_weather, "wd_data": result_wd, "ws_data": result_ws, "temp_data": result_temp}


# 城市实时数据分析
@app.route('/data/china/weather', methods=['post', 'get'])
def data_china_category():
    city = request.args.get('city')
    model = current_weather_service.select_current_weather_by_city(city)
    result_data = data_service.current_change_data(city)
    return {"model": model, "result_data": result_data}


# 城市实时数据分析
@app.route('/data/home/weather', methods=['post', 'get'])
def data_home_category():
    return data_service.top_page_data()


# 城市实时数据分析
@app.route('/data/weather/predict', methods=['post', 'get'])
def data_predict():
    city = request.args.get('city')
    return predict_service.predict(city)


# ----------------------------------------------分析相关模块结束----------------------------------------------


# ----------------------------------------------爬虫相关模块开始----------------------------------------------


from concurrent.futures import ThreadPoolExecutor


# 爬虫自动运行
def job_function():
    print("爬虫任务执行开始！")
    executor = ThreadPoolExecutor(2)
    executor.submit(spider_service.main_spider())


def task():
    scheduler = APScheduler()
    scheduler.init_app(app)
    # 定时任务，每隔600s执行1次
    scheduler.add_job(func=job_function, trigger='interval', seconds=600, id='my_cloud_spider_id')
    scheduler.start()


# 后台调用爬虫
@app.route('/spider/start', methods=["POST"])
def run_spider():
    executor = ThreadPoolExecutor(2)
    executor.submit(spider_service.main_spider())
    return '200'


# 写在main里面，IIS不会运行
task()
# run_spider()#启动项目就运行一次爬虫
# ----------------------------------------------爬虫相关模块结束----------------------------------------------
if __name__ == '__main__':
    # 端口号设置
    app.run(host="127.0.0.1", port=2000)
