import torch
import torch.nn as nn


class SEBlock(nn.Module):
    """Squeeze-and-Excitation 注意力模块，让网络自适应地学习通道权重。"""
    def __init__(self, channels, reduction=4):
        super(SEBlock, self).__init__()
        mid = max(channels // reduction, 8)
        self.squeeze = nn.AdaptiveAvgPool2d(1)
        self.excitation = nn.Sequential(
            nn.Linear(channels, mid, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(mid, channels, bias=False),
            nn.Hardsigmoid(inplace=True),
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        w = self.squeeze(x).view(b, c)
        w = self.excitation(w).view(b, c, 1, 1)
        return x * w


class InvertedResidual(nn.Module):
    """
    MobileNetV2 风格的倒残差块：
    1x1 升维 → 3x3 深度可分离卷积 → SE注意力 → 1x1 降维
    当 stride=1 且输入输出通道相同时使用残差连接。
    """
    def __init__(self, in_channels, out_channels, stride=1, expand_ratio=6, use_se=True):
        super(InvertedResidual, self).__init__()
        self.use_residual = (stride == 1 and in_channels == out_channels)
        mid_channels = in_channels * expand_ratio

        layers = []
        # 1x1 升维（当 expand_ratio > 1 时）
        if expand_ratio != 1:
            layers.extend([
                nn.Conv2d(in_channels, mid_channels, 1, bias=False),
                nn.BatchNorm2d(mid_channels),
                nn.ReLU6(inplace=True),
            ])

        # 3x3 深度可分离卷积
        layers.extend([
            nn.Conv2d(mid_channels, mid_channels, 3, stride=stride, padding=1,
                      groups=mid_channels, bias=False),
            nn.BatchNorm2d(mid_channels),
            nn.ReLU6(inplace=True),
        ])

        self.conv = nn.Sequential(*layers)

        # SE 注意力
        self.se = SEBlock(mid_channels) if use_se else nn.Identity()

        # 1x1 降维（线性瓶颈，不加激活函数）
        self.project = nn.Sequential(
            nn.Conv2d(mid_channels, out_channels, 1, bias=False),
            nn.BatchNorm2d(out_channels),
        )

    def forward(self, x):
        out = self.conv(x)
        out = self.se(out)
        out = self.project(out)
        if self.use_residual:
            out = out + x
        return out


class DWConv(nn.Module):
    """保留原始深度可分离卷积块以兼容旧代码。"""
    def __init__(self, in_channels, out_channels, stride=1):
        super(DWConv, self).__init__()
        self.depthwise = nn.Sequential(
            nn.Conv2d(in_channels, in_channels, kernel_size=3, stride=stride,
                      padding=1, groups=in_channels, bias=False),
            nn.BatchNorm2d(in_channels),
            nn.ReLU6(inplace=True),
        )
        self.pointwise = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU6(inplace=True),
        )

    def forward(self, x):
        x = self.depthwise(x)
        x = self.pointwise(x)
        return x


class StandardConv(nn.Module):
    """标准卷积块。"""
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1):
        super(StandardConv, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.conv(x)
