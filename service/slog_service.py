from entity.model import Notice
from utils.JsonUtils import get_class_one, get_class_list
from utils.PageUtils import get_page_start, PageData
from utils.Result import Result
from utils.SySQL import SQLManager

"""
日志数据相关业务逻辑服务层
"""


# 根据ID查询数据
def select_slog_by_id(id):
    sql = "SELECT * FROM slog WHERE id=%s"
    sqlManager = SQLManager()
    data = sqlManager.get_one(sql, id)
    slog = get_class_one(data, Notice)
    sqlManager.close()
    return slog


# 分页数据
def select_slog_list(page, limit, where):
    page, limit, where = get_page_start(int(page), int(limit), where)
    params_sql = get_search_params(where)
    data_sql = "SELECT * FROM slog WHERE 1=1 " + params_sql + " ORDER BY id DESC LIMIT %s,%s"
    count_sql = "SELECT COUNT(id) as i FROM slog WHERE 1=1 " + params_sql
    sqlManager = SQLManager()
    data = sqlManager.get_list(data_sql, (page, limit))  # 获取分页数据
    count = sqlManager.get_one(count_sql)['i']  # 获取数据总数
    slog = get_class_list(data, Notice)
    page_result = PageData(count, slog)
    return page_result


# 删除数据
def del_slog(id):
    sqlManager = SQLManager()
    sql = "DELETE FROM slog where id=%s"
    sqlManager.moddify(sql, id)
    sqlManager.close()
    return Result(True, "删除成功")


# 批量删除
def del_slog_list(ids):
    sqlManager = SQLManager()
    sql = "DELETE FROM slog where id in (" + ids + ")"
    sqlManager.moddify(sql)
    sqlManager.close()
    return Result(True, "删除成功")


# 获取单个数据
def get_slog(id):
    sqlManager = SQLManager()
    sql = "select * from `slog` where id=%s "
    data = sqlManager.get_one(sql, id)
    sqlManager.close()
    return data


# 查询条件处理
def get_search_params(where):
    sql = ''
    if where:
        if where['log'] and len(where['log']) > 0:
            sql = sql + " AND log like '%%" + where['log'] + "%%' "
    return sql
