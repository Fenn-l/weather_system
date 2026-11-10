import joblib

"""
多元线性回归预测
"""
import os
import machine_learning.deal_data as deal_data

# 加载模型

module_path = os.path.dirname(__file__)
path = module_path + '/model.joblib'
model = joblib.load(path)


# 预测数据(cityname, record_date, high, low, weather, wd, ws)
def predict(cityname, record_date, high, low, weather, wd, ws):
    city = cityname
    cityname, record_date, high, low, weather, wd, ws = deal_data.transformer_item(cityname, record_date, high, low,
                                                                                   weather, wd, ws)
    next_input = [float(cityname), float(record_date), float(high), float(low), float(weather), float(wd), float(ws)]
    result = []
    for i in range(1, 11):
        record_date, record_str = deal_data.getNextDay(i)
        pred_y = model.predict([next_input])[0]
        next_input = [float(cityname), float(record_date)]
        next_input.extend(pred_y)
        result.append(
            deal_data.de_transformer_item(city, record_str, pred_y[0], pred_y[1], pred_y[2], pred_y[3], pred_y[4]))
    return result


if __name__ == '__main__':
    print(predict("闵行", "2023-01-03", 34, 28, "阴", "东南风", 2))
