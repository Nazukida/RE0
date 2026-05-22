# 移动端轻量化宠物识别系统

本项目是一个完整的端到端深度学习项目，旨在构建一个轻量级的卷积神经网络（CNN），用于在移动设备上识别常见宠物（猫、狗）。项目涵盖了从数据加载、模型构建、训练调优到移动端部署准备的全流程。

## 项目结构

```
PetRecognitionSystem/
├── configs/                # 配置文件
│   └── config.yaml         # 超参数配置（学习率、Batch Size等）
├── data/                   # 数据存储
│   ├── raw/                # 原始数据
│   └── processed/          # 处理后的数据
├── docs/                   # 文档
├── src/                    # 源代码
│   ├── data/               # 数据处理模块
│   │   ├── loader.py       # Dataset 和 DataLoader 实现
│   │   └── transforms.py   # 数据增强策略
│   ├── models/             # 模型定义
│   │   ├── blocks.py       # 基础卷积块（含深度可分离卷积）
│   │   └── net.py          # MobilePetNet 网络架构
│   ├── training/           # 训练逻辑
│   │   ├── callbacks.py    # 早停（Early Stopping）等回调
│   │   └── trainer.py      # 训练与验证循环
│   ├── deploy/             # 部署模块
│   │   └── export.py       # 模型导出工具 (ONNX, TorchScript Mobile)
│   └── utils/              # 工具函数
│       └── logger.py       # 日志记录
├── train.py                # 项目入口脚本
├── requirements.txt        # 依赖库
└── README.md               # 项目说明
```

## 核心知识点与项目体现

### 1. PyTorch 卷积神经网络搭建
**知识点**：掌握 `torch.nn.Module` 的使用，理解卷积层、池化层、全连接层的作用。
**项目体现**：
- 在 `src/models/net.py` 中定义了 `MobilePetNet` 类。
- `src/models/blocks.py` 中实现了模块化的卷积块，体现了代码复用和模块化设计的思想。

### 2. 数据增强 (Data Augmentation)
**知识点**：通过对训练图片进行随机变换（裁剪、翻转、颜色抖动），增加数据多样性，提高模型泛化能力。
**项目体现**：
- `src/data/transforms.py` 定义了 `get_train_transforms`，包含 `RandomCrop`, `RandomHorizontalFlip`, `ColorJitter` 等操作。
- 这是一个**过拟合控制**的重要手段。

### 3. 模型训练标准工作流
**知识点**：完整的深度学习生命周期，包括 数据加载 -> 前向传播 -> 计算损失 -> 反向传播 -> 优化参数 -> 验证评估。
**项目体现**：
- `src/training/trainer.py` 中的 `train_epoch` 实现了训练步骤，`validate_epoch` 实现了验证步骤。
- 使用 `tqdm` 库展示进度条，使用 `logging` 模块记录训练过程。

### 4. 过拟合控制与超参数优化
**知识点**：如何防止模型在训练集表现好但在测试集表现差。
**项目体现**：
- **Early Stopping**: `src/training/callbacks.py` 实现了早停机制，当验证集 Loss 不再下降时自动停止训练，防止过拟合。
- **Learning Rate Decay**: `trainer.py` 中使用了 `ReduceLROnPlateau` 调度器，当指标停滞时自动降低学习率，属于超参数优化的动态调整策略。
- **Dropout**: 在 `net.py` 的分类器中使用了 `nn.Dropout(0.2)`。

### 5. 模型轻量化 (Model Lightweighting)
**知识点**：针对移动端算力受限的特点，设计参数量少、计算量低的模型。
**项目体现**：
- **深度可分离卷积 (Depthwise Separable Convolution)**: 在 `src/models/blocks.py` 中自定义了 `DWConv` 类。相比普通卷积，它大幅减少了参数量和乘加运算（MAdd），是 MobileNet 系列的核心组件。
- 网络设计倾向于“瘦高”结构，并在末端使用全局平均池化（GAP）替代庞大的全连接层。

### 6. 移动端部署准备
**知识点**：将训练好的 PyTorch 模型转换为通用的中间格式（如 ONNX）或移动端专用格式（TorchScript Mobile）。
**项目体现**：
- `src/deploy/export.py` 提供了 `export_to_onnx` 和 `export_to_torchscript_mobile` 函数。
- **ONNX**: 实现跨平台部署（如在 Android 上使用 ncnn 或 TNN 推理）。
- **TorchScript Mobile**: 针对 PyTorch Mobile 运行时进行了优化 (`optimize_for_mobile`)，可直接在 Android/iOS App 中加载。

## 运行指南

1. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

2. **开始训练**:
   ```bash
   python main.py --config configs/config.yaml --mode train
   ```
   *注意：如果没有数据集，代码会自动生成虚拟数据进行演示运行。*

3. **导出模型**:
   ```bash
   python main.py --config configs/config.yaml --mode export --checkpoint checkpoints/best_model.pt
   ```
