import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import torch
import os

# 配置 matplotlib 支持中文显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi', 'FangSong']  # 中文字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 假设你之前的模型代码保存在 neural_net.py 中
# 这里尝试导入，如果不存在请确保文件名正确
try:
    from neural_net import train_model
except ImportError:
    print("错误: 找不到 neural_net.py，请确保该文件在同一目录下。")

# --- GUI 应用程序类 ---
class DigitRecognizerApp:
    def __init__(self, root, model, device):
        self.root = root
        self.model = model
        self.device = device
        self.root.title("手写数字识别器 - AI 可视化")

        # 布局主框架
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack()

        # 1. 画板配置
        self.canvas_width = 280
        self.canvas_height = 280
        self.canvas_bg = "black"
        self.brush_color = "white"
        self.brush_size = 18

        # 创建 Canvas 组件
        self.canvas = tk.Canvas(
            self.main_frame, width=self.canvas_width, 
            height=self.canvas_height, bg=self.canvas_bg, cursor="cross"
        )
        self.canvas.grid(row=0, column=0, rowspan=4, padx=10, pady=10)
        self.canvas.bind("<B1-Motion>", self.draw)

        # 内存绘图对象 (用于将画板内容转为模型输入)
        self.image = Image.new("L", (self.canvas_width, self.canvas_height), self.canvas_bg)
        self.draw_obj = ImageDraw.Draw(self.image)

        # 2. 右侧按钮控制区域
        self.btn_frame = tk.Frame(self.main_frame)
        self.btn_frame.grid(row=0, column=1, sticky="n")

        self.predict_btn = tk.Button(
            self.btn_frame, text="识别数字 (Predict)", 
            command=self.predict, font=("Arial", 12), bg="#4CAF50", fg="white"
        )
        self.predict_btn.pack(pady=10, fill="x")

        self.clear_btn = tk.Button(
            self.btn_frame, text="清除画板 (Clear)", 
            command=self.clear_canvas, font=("Arial", 12)
        )
        self.clear_btn.pack(pady=10, fill="x")

        # 3. 结果显示
        self.result_label = tk.Label(
            self.main_frame, text="预测结果: None", 
            font=("Arial", 16, "bold"), fg="blue"
        )
        self.result_label.grid(row=1, column=1)

        # 4. 神经网络输入缩略图
        tk.Label(self.main_frame, text="模型眼中的输入 (28x28):", font=("Arial", 10)).grid(row=2, column=1, sticky="s")
        self.thumb_label = tk.Label(self.main_frame, bg="gray")
        self.thumb_label.grid(row=3, column=1)

        # 5. 初始化 Matplotlib 可视化窗口
        plt.ion() # 开启交互模式
        self.fig, self.ax = plt.subplots(1, 2, figsize=(8, 4))
        self.fig.canvas.manager.set_window_title("神经网络内部状态可视化")
        self.init_plot()

    # --- 绘图功能 ---
    def draw(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        # 在窗口画板上画圆
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.brush_color, outline=self.brush_color)
        # 在内存 PIL 图像上画圆 (同步数据)
        self.draw_obj.ellipse([x1, y1, x2, y2], fill=self.brush_color, outline=self.brush_color)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (self.canvas_width, self.canvas_height), self.canvas_bg)
        self.draw_obj = ImageDraw.Draw(self.image)
        self.result_label.config(text="预测结果: None")
        self.thumb_label.config(image='')
        self.init_plot()

    # --- 模型预测与可视化 ---
    def preprocess_image(self):
        # 核心步骤：将 280x280 的画板缩放为模型需要的 28x28
        img_resized = self.image.resize((28, 28), Image.Resampling.LANCZOS)
        img_array = np.array(img_resized)

        # 转化为 Tensor 并归一化（需与训练时保持一致）
        img_tensor = torch.tensor(img_array, dtype=torch.float32) / 255.0
        img_tensor = (img_tensor - 0.1307) / 0.3081
        img_tensor = img_tensor.unsqueeze(0).unsqueeze(0) # 形状变为 [1, 1, 28, 28]
        return img_tensor, img_resized

    def predict(self):
        input_tensor, pil_thumb = self.preprocess_image()

        # 更新左下角的小缩略图
        display_thumb = pil_thumb.resize((112, 112), Image.Resampling.NEAREST)
        self.photo_thumb = ImageTk.PhotoImage(display_thumb)
        self.thumb_label.config(image=self.photo_thumb)

        # 模型推理
        self.model.eval()
        with torch.no_grad():
            output = self.model(input_tensor.to(self.device))
            probs = torch.exp(output) # 因为模型返回了 log_softmax，这里用 exp 还原概率
            prediction = torch.argmax(probs, dim=1).item()
            confidence = probs[0][prediction].item()

        self.result_label.config(text=f"预测: {prediction}\n置信度: {confidence:.1%}")
        self.update_plot(input_tensor, probs)

    def init_plot(self):
        self.ax[0].clear()
        self.ax[0].set_title("输入热力图 (Input Heatmap)")
        self.ax[0].axis('off')
        self.ax[1].clear()
        self.ax[1].set_title("各数字预测概率 (Probs)")
        self.ax[1].set_ylim(0, 1)
        self.ax[1].set_xticks(range(10))
        self.fig.canvas.draw()

    def update_plot(self, input_tensor, probs):
        # 左图：显示模型真正看到的 28x28 矩阵
        img_data = input_tensor.squeeze().cpu().numpy()
        self.ax[0].imshow(img_data, cmap='viridis')

        # 右图：显示柱状图
        probs_data = probs.squeeze().cpu().numpy()
        self.ax[1].clear()
        self.ax[1].set_title("概率分布")
        self.ax[1].set_xticks(range(10))
        self.ax[1].set_ylim(0, 1.1)
        bars = self.ax[1].bar(range(10), probs_data, color='skyblue')
        bars[np.argmax(probs_data)].set_color('orange') # 最高概率涂成橘色

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

# --- 启动程序 ---
if __name__ == "__main__":
    print("正在初始化 AI 模型...")
    # 这里会调用之前写的 train_model 函数
    trained_model, device = train_model()

    print("正在启动 GUI 界面...")
    root = tk.Tk()
    app = DigitRecognizerApp(root, trained_model, device)

    # 退出时的清理工作
    def on_closing():
        plt.close('all')
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()