# 加载指定未知json文件
import json


def read_json(path="./china.json"):
    # 定义文件路径

    # 打开文件,r是读取,encoding是指定编码格式
    with open(path, 'r', encoding='utf-8') as fp:
        # load()函数将fp(一个支持.read()的文件类对象，包含一个JSON文档)反序列化为一个Python对象
        data = json.load(fp)
    fp.close()
    return data


# json对象转指定class对象
def parse_json_to_Obj(json_str, custom_object):
    json_object = json.dumps(json_str).__str__()
    # result = custom_object()
    # custom_object.__dict__ = json_object
    model = json.loads(json_object, object_hook=custom_object)
    return model


# 传入字典获取单个对象
def get_class_one(data, Model):
    try:
        model = Model()
        if isinstance(data, dict):
            model.__dict__ = data
        else:
            model = json.loads(data, object_hook=Model)
        return model
    except Exception as e:
        return None


# 传入字典数组获取数组对象
def get_class_list(arr, Model):
    try:
        data_arr = []
        for data in arr:
            model = Model()
            if isinstance(data, dict):
                model.__dict__ = data
            else:
                model = json.loads(data, object_hook=Model)
                return model
            data_arr.append(model)
        return data_arr
    except Exception as e:
        return None
