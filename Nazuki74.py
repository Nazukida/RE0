import numpy as np

a1 = np.array([1, 4, 2, 3, 5])
a2 = np.array([3.14, 4, 2, 3])
a3 = np.array([1, 2, 3, 4], dtype='float32')

print(a1)
print(a2)
print(a3)

a4 = np.array([1, 'siugfs', 3.14])
print(a4)
print(a4.dtype)

a5 = np.array([range(i, i+ 3) for i in [2, 4, 6, 8]])
print(a5)

print(np.zeros((3, 4), dtype=int))
print(np.arange(0, 20, 2))
print(np.linspace(0, 1, 5))
print(np.random.random((3, 4, 5)))
print(np.random.randint(0, 10, (4, 5)))
print(np.eye(10086))

x2 = np.array([[12,  5,  2,  4],
               [ 7,  6,  8,  8],
               [ 1,  6,  7,  7]])

print(x2[1:2, :3])    # 前2行，前3列
print(x2[:3, ::2])   # 所有行，每隔一列
print(x2[::-1, ::-1]) # 行列都反转

print(np.arange(0, 10).reshape(2, 5))

x = np.array([1, 2, 3])

print(x[np.newaxis, :])
print(x[:, np.newaxis])
print(x)

x = np.array([1, 2, 3])
y = np.array([3, 2, 1])

print(np.concatenate([x, y]))
print(np.vstack([x, y]))

print(np.sum(x2))

M = np.random.random((3, 4))
print(M)
print(M.sum())
print(M.sum(axis=0))
print(M.sum(axis=1))
print(M.min(axis=0))
print(M.max(axis=1))
print(M.shape)
print(M[:, np.newaxis].shape)

X = np.random.random((10, 3))   # 10个观测，3个特征
print(X)
Xmean = X.mean(0)               # 每列均值 → shape (3,)
print(Xmean)
X_centered = X - Xmean          # 广播！每行减去均值
print(X_centered)
X_centered.mean(0)               # ≈ [0, 0, 0]（验证）
print(X_centered.mean(0))

x = np.array([[5, 0, 3, 3],
              [7, 9, 3, 5],
              [2, 4, 7, 6]])
print(x < 6)  # 返回同形状的布尔数组

np.count_nonzero(x < 6)   # 小于6的元素个数 → 8
np.sum(x < 6)             # 等效（True当作1）
np.sum(x < 6, axis=1)     # 每行中 <6 的个数
print(np.count_nonzero(x < 6))
print(np.sum(x < 6))
print(np.sum(x < 6, axis=1))

X = np.arange(12).reshape((3, 4))
# [[ 0,  1,  2,  3],
#  [ 4,  5,  6,  7],
#  [ 8,  9, 10, 11]]

row = np.array([0, 1, 2])
col = np.array([2, 1, 3])
print(X[row, col])               # array([2, 5, 11]) ← X[0,2], X[1,1], X[2,3]
print(X[2, [2, 0, 1]])             # 第3行中取列2、0、1
print(X[1:, [2, 0, 1]])            # 花式索引 + 切片
mask = np.array([1, 0, 1, 0], dtype=bool)
print(X)
print(X[row[:, np.newaxis], mask])  # 花式索引 + 掩码
print(X.T)

print(np.linspace(1, 492, 29))
print(np.hstack([np.vstack([np.arange(0, 10), np.arange(10, 20), np.arange(20, 30)]).T, np.arange(30, 40)[:, np.newaxis]]))