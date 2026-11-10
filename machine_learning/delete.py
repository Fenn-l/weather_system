import csv

import pandas as pd

file_path = 'D:\\weather_system\\machine_learning\\historyweather.csv'

# 读取时指定列类型
df = pd.read_csv(file_path, header=None, dtype={3: float, 4: float}, quotechar="'")

# 直接保存会自动去除数值列的引号
df.to_csv(file_path,
         index=False,
         header=False,
         quoting=csv.QUOTE_NONNUMERIC,  # 只对非数字列加引号
         quotechar="'")
