from sklearn.tree import DecisionTreeRegressor
#specify the model. 
#For model reproducibility, set a numeric value for random_state when specifying the model
iowa_model = DecisionTreeRegressor(random_state = 1)

# Fit the model
iowa_model.fit(X,y)

# Check your answer
step_3.check()

predictions = iowa_model.predict(X)
print(predictions)

# 一、 初始查询与数据探索在加载数据（如 df = pd.read_csv('file.csv')）后，你会用到这些函数来“看清”数据。1. 快速预览df.head(n): 查看前 $n$ 行（默认 5 行）。df.tail(n): 查看最后 $n$ 行。df.sample(n): 随机抽取 $n$ 行进行检查，防止只看开头结尾产生的偏差。2. 结构与统计df.info(): 最重要。显示索引、列名、非空值数量以及每列的数据类型（Dtype）。df.describe(): 显示数值列的统计摘要（均值、标准差、最大/最小值、四分位数）。df.shape: 返回一个元组 (行数, 列数)。df.columns: 列出所有的列名。3. 数据质量检查df.isnull().sum(): 统计每一列中缺失值（NaN）的数量。df['column'].value_counts(): 统计某一列中每个唯一值出现的次数（非常适合分类数据）。df.nunique(): 统计每一列包含多少个不同的唯一值。二、 数据可视化Pandas 内置了基于 Matplotlib 的绘图功能，直接调用 .plot() 即可快速出图。1. 基础绘图语法Pythondf.plot(kind='图表类型', x='横轴列名', y='纵轴列名', title='标题')
# 2. 常用图表类型函数/参数图表类型最佳使用场景.plot(kind='line')折线图随时间变化的趋势（时间序列）。.plot(kind='bar')柱状图不同类别之间的数值比较。.plot(kind='hist')直方图查看单个数值变量的分布情况。.plot(kind='scatter')散点图观察两个数值变量之间的相关性。.plot(kind='box')箱线图识别离群值（异常值）和数据分散程度。3. 示例代码Pythonimport matplotlib.pyplot as plt

# # 绘制某两列的散点图
# df.plot(kind='scatter', x='Age', y='Salary', color='blue')
# plt.show()

# # 绘制直方图查看分布
# df['Income'].plot(kind='hist', bins=20)
# plt.title('Income Distribution')
# plt.show()