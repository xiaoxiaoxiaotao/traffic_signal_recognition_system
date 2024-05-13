import torch
import torchvision
from torch import nn
from torch.nn import Conv2d, MaxPool2d, Flatten, Linear, Sequential
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

train_data = torchvision.datasets.GTSRB("./data_image",split='train',download=True,
                                        transform=torchvision.transforms.ToTensor())
test_data = torchvision.datasets.GTSRB("./data_image",split='test',download=True,
                                        transform=torchvision.transforms.ToTensor())
#train_data = torchvision.datasets.CIFAR10(",/dataset",train=True,download=True,transform=torchvision.transforms.ToTensor())
#test_data = torchvision.datasets.CIFAR10(",/dataset",train=False,download=True,transform=torchvision.transforms.ToTensor())
train_data_size=len(train_data)
test_data_size=len(test_data)

print("训练数据集长度为：{}".format(train_data_size))
print("测试数据集长度为：{}".format(test_data_size))

#利用dataloader加载数据集

train_dataloader = DataLoader(train_data,batch_size=64)
test_datalader = DataLoader(test_data,batch_size=64)

#搭建神经网络

class Lzr(nn.Module):
    def __init__(self, *args, **kwargs):
        super(Lzr,self).__init__(*args, **kwargs)
        self.model = nn.Sequential(
            nn.Conv2d(3,32,5,1,2),
            nn.ReLU(),
            nn.MaxPool2d(2,2),

            nn.Conv2d(32,64,5),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Linear(64 * 5 * 5, 128),
            nn.ReLU(),
            nn.Linear(128, 84),
            nn.ReLU(),
            nn.Linear(84, 62)
        )

    def forward(self,x):
        x=self.model(x)
        return x


lzr= Lzr()

#损失函数
loss_fn = nn.CrossEntropyLoss()

#优化器
learning_rate = 1e-2;
optimizer= torch.optim.SGD(lzr.parameters(),lr=learning_rate)

total_train_step = 0
total_test_step = 0

epoch = 10

for i in range(epoch):
    print("第{}轮训练开始".format(i+1))
    for data in train_dataloader:
        imgs, targets = data
        outputs = lzr(imgs)
        loss = loss_fn(outputs,targets)
        #优化器优化模型
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_train_step=total_train_step+1
        print("训练次数：{}，Loss：{}".format(total_train_step,loss.item()))

