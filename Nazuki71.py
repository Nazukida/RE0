"""
在256x256像素画布上绘制最大正五边形并导出为透明PNG
"""

from PIL import Image, ImageDraw
import math

def draw_pentagon():
    # 画布大小
    size = 256
    
    # 创建透明背景的RGBA图像
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 中心点
    cx, cy = size / 2, size / 2
    
    # 最大半径（留一点边距避免被裁切）
    radius = size / 2 - 2
    
    # 计算正五边形的5个顶点
    # 从顶部开始（-90度），每隔72度一个顶点
    vertices = []
    for i in range(5):
        angle = math.radians(-90 + i * 72)  # 转换为弧度
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        vertices.append((x, y))
    
    # 绘制正五边形（填充白色，边框黑色）
    draw.polygon(vertices, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
    
    # 保存为透明PNG
    output_path = "pentagon.png"
    image.save(output_path, 'PNG')
    print(f"正五边形已保存到: {output_path}")
    
    return image

if __name__ == "__main__":
    draw_pentagon()
