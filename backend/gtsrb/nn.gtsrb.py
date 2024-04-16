import torch
import torchvision
from torch import nn
import numpy as np
from torch.nn import Conv2d, MaxPool2d, Flatten, Linear, Sequential
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms, datasets

transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
])
train_data = torchvision.datasets.GTSRB("./data_image", split='train', download=True,
                                        transform=transform)
test_data = torchvision.datasets.GTSRB("./data_image", split='test', download=True,
                                       transform=transform)
# train_data = torchvision.datasets.CIFAR10(",/dataset",train=True,download=True,transform=torchvision.transforms.ToTensor())
# test_data = torchvision.datasets.CIFAR10(",/dataset",train=False,download=True,transform=torchvision.transforms.ToTensor())
train_data_size = len(train_data)
test_data_size = len(test_data)
print(train_data)
print("训练数据集长度为：{}".format(train_data_size))
print("测试数据集长度为：{}".format(test_data_size))

# 利用dataloader加载数据集

train_dataloader = DataLoader(train_data, batch_size=32)
# train_dataloader = DataLoader(train_data, batch_size=32, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=32, shuffle=False)


# 搭建神经网络
# print(train_data.size)
class Lzr(nn.Module):
    def __init__(self):
        super(Lzr, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3, 16, 5),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 32, 5),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Flatten(),
            nn.Linear(32 * 5 * 5, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, 43)
        )

    def forward(self, x):
        return self.model(x)


lzr = Lzr()
loss_fn = nn.CrossEntropyLoss()
# 优化器
learning_rate = 1e-3
optimizer = torch.optim.SGD(lzr.parameters(), lr=learning_rate)

total_train_step = 0
total_test_step = 0

epoch = 100
writer = SummaryWriter("./logs_train")
for i in range(epoch):
    print("第{}轮训练开始".format(i + 1))
    for data in train_dataloader:
        imgs, targets = data
        outputs = lzr.forward(imgs)
        loss = loss_fn(outputs, targets)
        # 优化器优化模型
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_train_step = total_train_step + 1
        if total_train_step % 100 == 0:
            print("训练次数：{}，Loss：{}".format(total_train_step, loss.item()))
            writer.add_scalar("train_loss", loss.item(), total_train_step)

    # 测试步骤
    total_test_loss = 0
    total_accuracy = 0
    with torch.no_grad():
        for data in test_dataloader:
            imgs, targets = data
            outputs = lzr(imgs)
            loss = loss_fn(outputs, targets)
            total_test_loss = total_test_loss + loss.item()
            accuracy = (outputs.argmax(1) == targets).sum()
            total_accuracy = total_accuracy + accuracy

    print("整体测试集的Loss：{}".format(total_test_loss))
    print("整体测试集的正确率：{}".format(total_accuracy / test_data_size))

    writer.add_scalar("test_loss", total_test_loss, total_test_step)
    writer.add_scalar("test_accuracy", total_accuracy / test_data_size, total_test_step)
    total_test_step = total_test_step + 1

    torch.save(lzr, "gtsrb_{}.pth".format(i))
    print("模型已保存")
writer.close()
