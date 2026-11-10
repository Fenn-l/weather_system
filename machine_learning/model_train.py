from sklearn.linear_model import LinearRegression
import numpy as np
import joblib
import deal_data

"""
多元线性回归
"""
# 读取数据
print("[INFO] 多元线性回归预测气象数据-训练开始")
data = deal_data.transformer_data()

# 分割数据集合
train_data = []
test_data = []
for index, item in enumerate(data):
    if index % 5 == 0:  # 每5条数据，第6条保留为测试集合，也就是训练集：测试集=5：1
        test_data.append(item)
    else:
        train_data.append(item)

train_data = np.array(train_data)
test_data = np.array(test_data)

X = np.array(train_data[:, 0:7]).astype(float)
Y = np.array(train_data[:, 9:14]).astype(float)

test_X = np.array(test_data[:, 0:7]).astype(float)
text_Y = np.array(test_data[:, 9:14]).astype(float)

# 定义算法模型
model = LinearRegression()
# 喂入模型数据
model.fit(X, Y)
joblib.dump(model, "./model.joblib")

# 测试集上模型评分
print("[INFO] 模型EMS损失值（模型评分越低越好）：", abs(model.score(test_X, text_Y)))
print("[INFO] 多元线性回归预测气象数据-训练完成")
