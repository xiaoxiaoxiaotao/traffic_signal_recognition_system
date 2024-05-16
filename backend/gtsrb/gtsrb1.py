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
        conv_channel = [64, 128, 256]
        self.model = nn.Sequential(
            # padding=图像周边填充像素，上下左右都填充了
            nn.Conv2d(in_channels=3, out_channels=conv_channel[0], kernel_size=5, padding=2),
            nn.BatchNorm2d(num_features=conv_channel[0]),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(conv_channel[0], conv_channel[1], 5, padding=2),
            nn.BatchNorm2d(conv_channel[1]),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(conv_channel[1], conv_channel[2], 5, padding=2),
            nn.BatchNorm2d(conv_channel[2]),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Flatten(),

            # 64*64，3次Maxpool，最后8*8
            nn.Linear(conv_channel[2] * 8 * 8, 200),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(200, 84),
            nn.ReLU(),
            nn.Linear(84, 43)
        )

    def forward(self, x):
        return self.model(x)

    def train_module(self, epoch: int, learning_rate: float, train_data, test_data, if_cuda: bool = False):
        train_data_size = len(train_data)
        test_data_size = len(test_data)
        print(train_data)
        print("训练数据集长度为：{}".format(train_data_size))
        print("测试数据集长度为：{}".format(test_data_size))

        # 利用dataloader加载数据集
        train_dataloader = DataLoader(train_data, batch_size=50, shuffle=True)
        test_dataloader = DataLoader(test_data, batch_size=50, shuffle=False)

        optimizer = torch.optim.SGD(self.parameters(), lr=learning_rate)
        total_train_step = 0
        epoch_train_step = 0

        writer = SummaryWriter(os.path.join('logs_train'))
        for i in range(epoch):
            print("第{}轮训练开始".format(i + 1))
            epoch_loss = 0
            for data in train_dataloader:
                imgs, targets = data
                # cuda
                if if_cuda:
                    imgs, targets = imgs.cuda(), targets.cuda()
                outputs = self.forward(imgs)
                loss = self.loss_fn(outputs, targets)
                # 优化器优化模型
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                step_loss = loss.item()
                epoch_loss += step_loss
                print("Epoch:{}，Step：{}（总{}），Loss：{}".format(i + 1, epoch_train_step, total_train_step, step_loss))
                if total_train_step % 100 == 0:
                    writer.add_scalar("train_loss", loss.item(), i + 1, total_train_step)
                total_train_step = total_train_step + 1
                epoch_train_step = epoch_train_step + 1

            print("========================")
            print("Epoch{}：训练总Loss：{}".format(i, epoch_loss))
            writer.add_scalar("train_epoch_loss", epoch_loss, i + 1)

            test_accuracy, total_test_loss = self.test_accu(test_dataloader, test_data_size, if_cuda)
            print("Epoch{}：测试准确度{}，测试Loss：{}".format(i + 1, test_accuracy, total_test_loss))
            writer.add_scalar("test_loss", total_test_loss, i + 1)
            writer.add_scalar("test_accuracy", test_accuracy, i + 1)

            epoch_train_step = 0

            file_name = "gtsrb1_{epoch}_{time}-{train_epoch_loss}_{test_accuracy}%.pth"\
                .format(epoch=i + 1, time=time.time(), train_epoch_loss=epoch_loss, test_accuracy=test_accuracy * 100)
            torch.save(self, os.path.join('trained_modules1', file_name))
            print("模型已保存到：" + os.path.join('trained_modules1', file_name))
            print("========================")
        writer.close()

    def test_accu(self, test_dataloader, test_data_size: int, if_cuda: bool = False) -> (int, int):
        total_test_loss = 0
        total_right = 0
        with torch.no_grad():
            for data in test_dataloader:
                imgs, targets = data
                # cuda
                if if_cuda:
                    imgs, targets = imgs.cuda(), targets.cuda()
                outputs = self.forward(imgs)
                loss = self.loss_fn(outputs, targets)
                total_test_loss = total_test_loss + loss.item()
                if_right = (outputs.argmax(1) == targets).sum()
                total_right = total_right + if_right
            total_accuracy = total_right / test_data_size
        return total_accuracy, total_test_loss


if __name__ == "__main__":
    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
    ])
    train_data = torchvision.datasets.GTSRB("./data_image", split='train', download=True,
                                            transform=transform)
    test_data = torchvision.datasets.GTSRB("./data_image", split='test', download=True,
                                           transform=transform)

    lzr = Lzr()

    if_cuda = torch.cuda.is_available()
    if if_cuda:
        print("在cuda上运行。")
        lzr = lzr.to("cuda")
    else:
        print("在cpu上运行。")

    lzr.train_module(100, 0.09, train_data, test_data, if_cuda)  # batch_size在方法里面

