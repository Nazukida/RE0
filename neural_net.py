import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import os

# 1. 定义网络结构
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        # 将图片展开成一维向量: [batch_size, 784]
        x = x.view(-1, 28 * 28)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        # 注意：使用了 CrossEntropyLoss 时，其实不需要在这里手动做 log_softmax
        # 但为了保持你原始代码逻辑一致，这里保留返回
        return torch.log_softmax(x, dim=1)

# 2. 训练与加载逻辑
def train_model():
    """训练模型或加载已有模型"""
    model_path = "mnist_model.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Net().to(device)

    # 检查是否存在已有的权重文件
    if os.path.exists(model_path):
        print(f"发现已保存的模型 {model_path}，正在加载...")
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()
        return model, device

    print("未发现模型，开始下载数据集并训练 (准确率目标 > 90%)...")

    # 数据预处理
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    # 加载 MNIST 数据集
    train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)

    # 定义优化器和损失函数
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    # 开始训练
    model.train()
    epochs = 6
    for epoch in range(epochs):
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()           # 梯度清零
            output = model(data)            # 前向传播
            loss = criterion(output, target) # 计算损失
            loss.backward()                 # 反向传播
            optimizer.step()                # 更新参数

            if batch_idx % 100 == 0:
                print(f'Epoch {epoch + 1}/{epochs} | Batch {batch_idx} | Loss: {loss.item():.4f}')

    print("训练完成，正在保存模型...")
    torch.save(model.state_dict(), model_path)
    model.eval()
    return model, device

# 3. 运行入口
if __name__ == "__main__":
    trained_model, target_device = train_model()
    print(f"模型已就绪，运行设备: {target_device}")