import pandas as pd
import numpy as np

data = pd.Series([0.25, 0.5, 0.75, 1.0])
# 输出：
# 0    0.25
# 1    0.50
# 2    0.75
# 3    1.00
# dtype: float64
print(data)
print(pd.Series(5, index=[100, 200, 300]))
print(pd.Series({2:'a', 1:'b', 3:'c'}))
print(pd.Series({2:'a', 1:'b', 3:'c'}, index=[3, 2]))

population = {'California': 38332521, 'Texas': 26448193, 'New York': 19651127, 'Florida': 19552860, 'Illinois': 12882135}
area = {'California': 423967, 'Texas': 695662, 'New York': 141297, 'Florida': 170312, 'Illinois': 149995}
states = pd.DataFrame({'population': population, 'area': area})
#             population    area
# California    38332521  423967
# Texas         26448193  695662
# ...
print(states)
print(states['area'])
print(states.area)

print(pd.DataFrame([{'a': 1, 'b': 2}, {'b': 3, 'c': 4}]))
print(pd.DataFrame(np.random.rand(3, 2), columns=['foo', 'bar'], index=['a', 'b', 'c']))
data.index = ['a', 'b', 'c', 'd']
print(data['b'])
print('a' in data)
print(data.keys())          # 所有键
print(list(data.items()))   # 键值对列表

A = pd.Series([2, 4, 6], index=[0, 1, 2])
B = pd.Series([1, 3, 5], index=[1, 2, 3])
print(A + B)
# 0    NaN    ← 只有A有index 0
# 1    5.0    ← 4+1
# 2    9.0    ← 6+3
# 3    NaN    ← 只有B有index 3

# ========== MultiIndex 示例 ==========

# 创建 MultiIndex
index = pd.MultiIndex.from_product([['a','b'], [1,2]])
print("MultiIndex:\n", index)

# 用 MultiIndex 创建 Series
pop = pd.Series([100, 200, 300, 400], index=index)
print("\nMultiIndex Series:\n", pop)

# 命名层级
pop.index.names = ['letter', 'number']
print("\n命名层级后:\n", pop)

# 访问
print("\n精确索引 pop['a', 1]:", pop['a', 1])
print("部分索引 pop['a']:\n", pop['a'])
print("跨层级 pop[:, 2]:\n", pop[:, 2])

# 重要转换
print("\nSeries.unstack() → DataFrame:\n", pop.unstack())
df = pop.unstack()
print("\nDataFrame.stack() → MultiIndex Series:\n", df.stack())
print("\nSeries.reset_index() → 普通列:\n", pop.reset_index())

# 普通列 → MultiIndex
df_flat = pop.reset_index()
df_multi = df_flat.set_index(['letter', 'number'])
print("\nset_index → MultiIndex:\n", df_multi)

# ⚠️ 切片前必须排序！
# 创建一个未排序的 MultiIndex
unsorted_idx = pd.MultiIndex.from_tuples([('b', 2), ('a', 1), ('b', 1), ('a', 2)])
unsorted_s = pd.Series([10, 20, 30, 40], index=unsorted_idx)
print("\n未排序:\n", unsorted_s)
sorted_s = unsorted_s.sort_index()
print("排序后:\n", sorted_s)
print("排序后切片 sorted_s['a':'b']:\n", sorted_s['a':'b'])