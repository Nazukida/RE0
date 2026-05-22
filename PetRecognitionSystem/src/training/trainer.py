import torch
import torch.nn as nn
import torch.optim as optim
from torch.amp.grad_scaler import GradScaler
from torch.amp.autocast_mode import autocast
from tqdm import tqdm
import os
from .callbacks import EarlyStopping


class Trainer:
    def __init__(self, model, train_loader, val_loader, config, device):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config
        self.device = device

        # 标签平滑：防止模型过度自信，提升泛化能力
        self.criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

        # AdamW：解耦权重衰减，正则化效果优于 Adam
        self.optimizer = optim.AdamW(
            self.model.parameters(),
            lr=config['learning_rate'],
            weight_decay=1e-4,
        )

        # 余弦退火学习率调度：平滑衰减，避免阶梯式跳变
        self.scheduler = optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer,
            T_max=config['epochs'],
            eta_min=1e-6,
        )

        # 混合精度训练：在 GPU 上显著加速并减少显存占用
        self.use_amp = (device.type == 'cuda')
        self.device_type = device.type
        self.scaler = GradScaler(device.type, enabled=self.use_amp)

        os.makedirs(config['save_dir'], exist_ok=True)
        self.early_stopping = EarlyStopping(
            patience=config['early_stopping_patience'],
            verbose=True,
            path=os.path.join(config['save_dir'], 'best_model.pt'),
        )

    def train_epoch(self):
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in tqdm(self.train_loader, desc="Training"):
            inputs, labels = inputs.to(self.device), labels.to(self.device)

            self.optimizer.zero_grad(set_to_none=True)

            with autocast(device_type=self.device_type, enabled=self.use_amp):
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)

            self.scaler.scale(loss).backward()
            # 梯度裁剪：防止梯度爆炸
            self.scaler.unscale_(self.optimizer)
            nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.scaler.step(self.optimizer)
            self.scaler.update()

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        train_loss = running_loss / len(self.train_loader)
        train_acc = correct / total
        return train_loss, train_acc

    def validate_epoch(self):
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for inputs, labels in tqdm(self.val_loader, desc="Validation"):
                inputs, labels = inputs.to(self.device), labels.to(self.device)

                with autocast(device_type=self.device_type, enabled=self.use_amp):
                    outputs = self.model(inputs)
                    loss = self.criterion(outputs, labels)

                running_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()

        val_loss = running_loss / len(self.val_loader)
        val_acc = correct / total
        return val_loss, val_acc

    def run(self):
        for epoch in range(self.config['epochs']):
            lr = self.optimizer.param_groups[0]['lr']
            print(f"\nEpoch {epoch+1}/{self.config['epochs']}  lr={lr:.2e}")

            train_loss, train_acc = self.train_epoch()
            val_loss, val_acc = self.validate_epoch()

            print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f}")
            print(f"Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:.4f}")

            self.scheduler.step()
            self.early_stopping(val_loss, self.model)

            if self.early_stopping.early_stop:
                print("Early stopping triggered")
                break
