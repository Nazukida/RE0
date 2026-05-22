import torch
import torch.nn as nn
from .blocks import StandardConv, InvertedResidual


class MobilePetNet(nn.Module):
    """
    优化版轻量级 CNN 架构，基于 MobileNetV2 设计理念：
    - 倒残差块 + 残差连接改善梯度流动
    - SE 注意力模块自适应学习通道权重
    - 精简通道数（最大 512），适配二分类任务
    """
    def __init__(self, num_classes=2):
        super(MobilePetNet, self).__init__()

        # Stem: 标准卷积降采样
        self.stem = StandardConv(3, 32, stride=2)  # 224→112

        # 倒残差特征提取层
        # (in_ch, out_ch, stride, expand_ratio, repeat)
        block_configs = [
            (32,  16,  1, 1, 1),    # 112×112
            (16,  24,  2, 6, 2),    # 112→56
            (24,  32,  2, 6, 3),    # 56→28
            (32,  64,  2, 6, 4),    # 28→14
            (64,  96,  1, 6, 3),    # 14×14
            (96,  160, 2, 6, 3),    # 14→7
            (160, 320, 1, 6, 1),    # 7×7
        ]

        layers = []
        for in_c, out_c, s, t, n in block_configs:
            for i in range(n):
                stride = s if i == 0 else 1
                inp = in_c if i == 0 else out_c
                layers.append(InvertedResidual(inp, out_c, stride=stride, expand_ratio=t))

        self.features = nn.Sequential(*layers)

        # 1x1 卷积升维 + 全局池化
        self.head_conv = nn.Sequential(
            nn.Conv2d(320, 512, 1, bias=False),
            nn.BatchNorm2d(512),
            nn.ReLU6(inplace=True),
        )
        self.pool = nn.AdaptiveAvgPool2d(1)

        self.classifier = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(512, num_classes),
        )

        self._init_weights()

    def _init_weights(self):
        """Kaiming 初始化，加速收敛。"""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, x):
        x = self.stem(x)
        x = self.features(x)
        x = self.head_conv(x)
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


def get_model(config):
    return MobilePetNet(num_classes=config['num_classes'])
