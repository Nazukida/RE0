import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
x = np.linspace(0, 5, 10)
y = x ** 2
fig, ax = plt.subplots()    # 创建一个图形(figure)和一个坐标轴(axes)
plt.plot(x, y, 'r')         # 画 y vs x 的曲线，'r' 表示红色
plt.xlabel('x')             # x 轴标签
plt.ylabel('y')             # y 轴标签
plt.title('Hello World')
plt.show()

plt.subplot(1, 2, 1)        # 1行2列，选第1个位置
plt.plot(x, y, 'r--')       # 红色虚线
plt.subplot(1, 2, 2)        # 1行2列，选第2个位置
plt.plot(y, x, 'g*-')       # 绿色，带星号标记的实线
plt.show()

x = np.linspace(0, 2, 100)
fig, ax = plt.subplots()
plt.plot(x, x, 'r')       # 红色线性: y = x
plt.plot(x, x**2, 'g')    # 绿色二次: y = x²
plt.plot(x, x**3, 'b')    # 蓝色三次: y = x³
plt.show()

x = np.linspace(0, 5, 10)
y = x ** 2

fig = plt.figure()                        # 创建空画布
axes = fig.add_axes([0.1, 0.2, 0.8, 0.8]) # [左, 下, 宽, 高]，范围 0~1
axes.plot(x, y, 'r')                      # 在该坐标轴上画图
axes.set_xlabel('x')
axes.set_ylabel('y')
axes.set_title('hello world')
plt.show()

fig = plt.figure()
axes1 = fig.add_axes([0.1, 0.2, 0.8, 0.8])  # 主图
axes2 = fig.add_axes([0.2, 0.5, 0.4, 0.3])  # 插入的小图

# 主图
axes1.plot(x, y, 'r')
axes1.set_xlabel('x')
axes1.set_ylabel('y')
axes1.set_title('title')

# 小图
axes2.plot(y, x, 'g')
axes2.set_xlabel('y')
axes2.set_ylabel('x')
axes2.set_title('insert title')
plt.show()

x = np.linspace(0, 2, 100)
fig = plt.figure()
axes = fig.add_axes([0.1, 0.2, 0.8, 0.8])
axes.plot(x, x, 'r')
axes.plot(x, x**2, 'g')
axes.plot(x, x**3, 'b')
plt.show()

fig, ax = plt.subplots()
ax.plot(x, x**2, label="y = x**2")    # label 参数定义图例文字
ax.plot(x, x**3, label="y = x**3")
ax.legend(loc=2)                        # loc=2 表示左上角
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('title')
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].plot(x, x**2, x, np.exp(x))
axes[0].set_title("Normal scale")

axes[1].plot(x, x**2, x, np.exp(x))
axes[1].set_yscale('log')                    # y 轴设为对数刻度
axes[1].set_title("Logarithmic scale (y)")
plt.show()

xx  = np.linspace(0, 5, 100)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].scatter(xx, xx + 0.25*np.random.randn(len(xx)))
axes[0].set_title("Scatter plot")
plt.show()

fig = plt.figure()
ax = fig.add_axes([0.0, 0.0, 0.6, 0.6], polar=True)  # polar=True！
t = np.linspace(0, 2 * np.pi, 100)
ax.plot(t, t, color='blue', lw=3)
plt.show()

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)     # 创建网格
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)  # 添加颜色条
plt.show()

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(1, 1, 1, projection='3d')
p = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
plt.show()

from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'ro')

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update,
                    frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()