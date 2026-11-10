import json


class PageData:

    def __init__(self, count, models):
        self.count = count
        self.data = deal_data(models)
        self.code = 0
        self.msg = "查询成功"

    def get(self):
        return self.__dict__


def deal_data(models):
    page_list = []
    if models:
        for item in models:
            page_list.append(item.__dict__)
    return page_list


def get_page_start(page=1, limit=15, where=''):
    start_page = 0
    if page:
        start_page = (page - 1) * limit

    if where and len(where) > 0:
        where = json.loads(where)
    return start_page, limit, where
