import json

from flask import jsonify


class Result:
    def __init__(self, success=True, msg="操作成功", data=[]):
        self.success = success
        self.msg = msg
        self.data = data

    def get(self):
        return self.__dict__
