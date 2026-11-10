import pandas as pd

# 读取CSV文件
file_path = 'D:\\weather_system\\machine_learning\\historyweather.csv'
df = pd.read_csv(file_path, header=None)


# 定义一个函数来替换日期中的 '/'
def replace_slash_with_dash(date_str):
    if isinstance(date_str, str):  # 确保是字符串类型
        return date_str.replace('/', '-')
    return date_str


# 假设日期在第三列（索引为2），以及第九列（索引为8）
df[2] = df[2].apply(replace_slash_with_dash)
df[8] = df[8].apply(replace_slash_with_dash)

# 将修改后的数据保存回CSV文件
df.to_csv(file_path, index=False, header=False)
