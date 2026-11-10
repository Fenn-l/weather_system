from entity.model import Notice
from utils.JsonUtils import get_class_one, get_class_list
from utils.PageUtils import get_page_start, PageData
from utils.Result import Result
from utils.SySQL import SQLManager

"""
公告数据相关业务逻辑服务层
"""


# 根据ID查询数据
def select_notice_by_id(id):
    sql = "SELECT * FROM notice WHERE id=%s"
    sqlManager = SQLManager()
    data = sqlManager.get_one(sql, id)
    notice = get_class_one(data, Notice)
    sqlManager.close()
    return notice


# 分页数据
def select_notice_list(page, limit, where):
    page, limit, where = get_page_start(int(page), int(limit), where)
    params_sql = get_search_params(where)
    data_sql = "SELECT * FROM notice WHERE 1=1 " + params_sql + " ORDER BY id DESC LIMIT %s,%s"
    count_sql = "SELECT COUNT(id) as i FROM notice WHERE 1=1 " + params_sql
    sqlManager = SQLManager()
    data = sqlManager.get_list(data_sql, (page, limit))  # 获取分页数据
    count = sqlManager.get_one(count_sql)['i']  # 获取数据总数
    notice = get_class_list(data, Notice)
    page_result = PageData(count, notice)
    return page_result


# 插入数据
def insert_notice(data):
    sqlManager = SQLManager()
    sql = "INSERT INTO notice (title,content,user_name) VALUES (%s,%s,%s)"
    sqlManager.instert(sql, (data['title'], data['content'], data['user_name']))
    sqlManager.close()
    return Result(True, "添加成功")


# 修改数据
def edit_notice(data):
    sqlManager = SQLManager()
    sql = "update notice SET title=%s,content=%s,user_name=%s where id=%s"
    sqlManager.moddify(sql, (data['title'], data['content'], data['user_name'], data['id']))
    sqlManager.close()
    return Result(True, "修改成功")


# 删除数据
def del_notice(id):
    sqlManager = SQLManager()
    sql = "DELETE FROM notice where id=%s"
    sqlManager.moddify(sql, id)
    sqlManager.close()
    return Result(True, "删除成功")


# 批量删除
def del_notice_list(ids):
    sqlManager = SQLManager()
    sql = "DELETE FROM notice where id in (" + ids + ")"
    sqlManager.moddify(sql)
    sqlManager.close()
    return Result(True, "删除成功")


# 获取单个数据
def get_notice(id):
    sqlManager = SQLManager()
    sql = "select * from `notice` where id=%s "
    data = sqlManager.get_one(sql, id)
    sqlManager.close()
    return data


# 获取最新的单个数据
def get_notice_by_new():
    sqlManager = SQLManager()
    sql = "select * from `notice` order by create_time desc limit 1"
    data = sqlManager.get_one(sql)
    sqlManager.close()
    return Result(True, '', data)


# 查询条件处理
def get_search_params(where):
    sql = ''
    if where:
        if where['title'] and len(where['title']) > 0:
            sql = sql + " AND title like '%%" + where['title'] + "%%' "
        if where['content'] and len(where['content']) > 0:
            sql = sql + " AND content like '%%" + where['content'] + "%%' "
        if where['user_name'] and len(where['user_name']) > 0:
            sql = sql + " AND title user_name '%%" + where['user_name'] + "%%' "
    return sql
