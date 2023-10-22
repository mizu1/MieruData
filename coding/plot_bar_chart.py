# filename: plot_bar_chart.py

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(r'd:\CodeFiles\CondaProgram\MieruData\data\inputData\Mytest.csv')

# 绘制柱状图
plt.bar(data['x'], data['y'])

# 保存图片
plt.savefig('/static/img/createdImg/created.png')

# 打印提示信息
print('图像已绘制')