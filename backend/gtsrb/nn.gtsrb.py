import torch
import torchvision
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms

import time
import os

# 搭建神经网络
# print(train_data.size)
class Lzr(nn.Module):
    def __init__(self):
        super(Lzr, self).__init__()
        self.loss_fn = nn.CrossEntropyLoss()
        self.model = nn.Sequential(
            nn.Conv2d(3, 16, 5, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(16, 32, 5, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Flatten(),

            nn.Linear(32 * 8 * 8, 120),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, 43)
        )

    def forward(self, x):
        return self.model(x)

    def train_module(self, epoch: int, learning_rate: float, train_data, test_data):
        train_data_size = len(train_data)
        test_data_size = len(test_data)
        print(train_data)
        print("训练数据集长度为：{}".format(train_data_size))
        print("测试数据集长度为：{}".format(test_data_size))

        # 利用dataloader加载数据集
        train_dataloader = DataLoader(train_data, batch_size=32, shuffle=True)
        test_dataloader = DataLoader(test_data, batch_size=32, shuffle=False)

        optimizer = torch.optim.SGD(self.parameters(), lr=learning_rate)
        total_train_step = 0
        total_test_step = 0

        writer = SummaryWriter(os.path.join('logs_train'))
        for i in range(epoch):
            print("第{}轮训练开始".format(i + 1))
            for data in train_dataloader:
                imgs, targets = data
                outputs = self.forward(imgs)
                loss = self.loss_fn(outputs, targets)
                # 优化器优化模型
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_train_step = total_train_step + 1
                if total_train_step % 100 == 0:
                    print("训练次数：{}，Loss：{}".format(total_train_step, loss.item()))
                    writer.add_scalar("train_loss", loss.item(), total_train_step)
            total_accuracy, total_test_loss = self.test_accu(test_dataloader, test_data_size)
            writer.add_scalar("test_loss", total_test_loss, total_test_step)
            writer.add_scalar("test_accuracy", total_accuracy, total_test_step)
            total_test_step = total_test_step + 1
            file_name = "gtsrb_{epoch}_{time}.pth".format(epoch=i, time=time.time())
            torch.save(self, os.path.join('trained_modules', file_name))
            print("模型已保存到" + os.path.join('trained_modules', file_name))
        writer.close()

    def test_accu(self, test_dataloader, test_data_size: int) -> (int, int):
        total_test_loss = 0
        total_right = 0
        with torch.no_grad():
            for data in test_dataloader:
                imgs, targets = data
                outputs = self.forward(imgs)
                loss = self.loss_fn(outputs, targets)
                total_test_loss = total_test_loss + loss.item()
                if_right = (outputs.argmax(1) == targets).sum()
                total_right = total_right + if_right
            total_accuracy = total_right / test_data_size
        return total_accuracy, total_test_loss


if __name__ == "__main__":
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
    ])
    train_data = torchvision.datasets.GTSRB("./data_image", split='train', download=True,
                                            transform=transform)
    test_data = torchvision.datasets.GTSRB("./data_image", split='test', download=True,
                                           transform=transform)

    lzr = Lzr()
    lzr.train_module(10000, 10e-3, train_data, test_data)

