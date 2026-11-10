import hashlib

from flask import session

from entity.model import User
from utils.JsonUtils import get_class_one, get_class_list, parse_json_to_Obj
from utils.PageUtils import get_page_start, PageData
from utils.Result import Result
from utils.SySQL import SQLManager

"""
西安区域气象数据相关业务逻辑服务层
"""
is_encrypt = False  # 是否加密


# 根据用户账号查询数据
def select_user_by_account_password(data):
    password = data['password']
    account = data['account']
    if is_encrypt:
        md = hashlib.md5(data['password'].encode())
        password = md.hexdigest()  # 单纯的MD5加密
    sql = "SELECT * FROM user WHERE account=%s and password=%s"
    sqlManager = SQLManager()
    data = sqlManager.get_one(sql, (account, password))
    user = get_class_one(data, User)
    sqlManager.close()
    if user:
        return Result(True, "登陆成功", user.__dict__)
    else:
        return Result(False, "请输入正确的账号密码")


# 注册用户
def insert_user(data):
    sqlManager = SQLManager()
    check_sql = "SELECT count(id) as i FROM user where account=%s or mail=%s"
    count = sqlManager.get_one(check_sql, (data['account'], data['mail']))['i']
    if count > 0:
        return Result(False, "账号或邮箱重复")
    sql = "INSERT INTO user (name,account,password,company,mail,type,status) VALUES (%s,%s,%s,%s,%s,1,1)"
    sqlManager.instert(sql, (data['name'], data['account'], data['password'], data['company'], data['mail']))
    sqlManager.close()
    return Result(True, "注册成功")


def select_user_list(page, limit, where):
    page, limit, where = get_page_start(int(page), int(limit), where)
    params_sql = get_search_params(where)
    data_sql = "SELECT * FROM user WHERE 1=1 " + params_sql + " ORDER BY id DESC LIMIT %s,%s"
    count_sql = "SELECT COUNT(id) as i FROM user WHERE 1=1 " + params_sql
    sqlManager = SQLManager()
    data = sqlManager.get_list(data_sql, (page, limit))  # 获取分页数据
    count = sqlManager.get_one(count_sql)['i']  # 获取数据总数
    user = get_class_list(data, User)
    page_result = PageData(count, user)
    return page_result


# 修改用户信息
def edit_user(data):
    sqlManager = SQLManager()
    sql = "update user SET name=%s,company=%s,password=%s,mail=%s,type=%s,status=%s where id=%s"
    sqlManager.moddify(sql, (data['name'], data['company'], data['password'], data['mail'], data['type'],
                             data['status'], data['id']))
    sqlManager.close()
    return Result(True, "修改成功")


# 删除用户
def del_user(id):
    sqlManager = SQLManager()
    sql = "DELETE FROM user where id=%s"
    sqlManager.moddify(sql, id)
    sqlManager.close()
    return Result(True, "删除成功")


# 批量删除
def del_user_list(ids):
    sqlManager = SQLManager()
    sql = "DELETE FROM user where id in (" + ids + ")"
    sqlManager.moddify(sql)
    sqlManager.close()
    return Result(True, "删除成功")


# 获取单个数据
def get_user(id):
    sqlManager = SQLManager()
    sql = "select * from `user` where id=%s "
    data = sqlManager.get_one(sql, id)
    sqlManager.close()
    return data


# 查询条件处理
def get_search_params(where):
    sql = ''
    if where:
        if where['name'] and len(where['name']) > 0:
            sql = sql + " AND name like '%%" + where['name'] + "%%' "
        if where['account'] and len(where['account']) > 0:
            sql = sql + " AND account like '%%" + where['account'] + "%%' "
        if where['company'] and len(where['company']) > 0:
            sql = sql + " AND company like '%%" + where['company'] + "%%' "
        if where['mail'] and len(where['mail']) > 0:
            sql = sql + " AND mail like '%%" + where['mail'] + "%%' "
    return sql

# 修改密码
def reset_password(op, np, ap):
    if is_encrypt:
        op = hashlib.md5(op.encode())
        op = op.hexdigest()  # 单纯的MD5加密
        np = hashlib.md5(np.encode())
        np = np.hexdigest()  # 单纯的MD5加密
        ap = hashlib.md5(ap.encode())
        ap = ap.hexdigest()  # 单纯的MD5加密
    try:
        user = get_class_one(session['user'], User)
        if user.password != op:
            return Result(False, '旧密码错误')
        elif np != ap:
            return Result(False, '两次密码不一致')
        else:
            user.password = np
            session['user'] = user.__dict__
            sql = 'update user set password = %s where account=%s'
            sqlManager = SQLManager()
            sqlManager.moddify(sql, (np, user.account))
            sqlManager.close()
            return Result(True, '修改成功')
    except Exception as e:
        return Result(False, '还未登录用户')