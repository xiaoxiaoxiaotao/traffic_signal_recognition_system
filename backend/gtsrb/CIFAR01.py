import torch
import torchvision
from torch import nn
from torch.nn import Conv2d, MaxPool2d, Flatten, Linear, Sequential
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

#train_data = torchvision.datasets.GTSRB("./data_image",split='train',download=True,
                                        #transform=torchvision.transforms.ToTensor())
#test_data = torchvision.datasets.GTSRB("./data_image",split='test',download=True,
                                        #transform=torchvision.transforms.ToTensor())
train_data = torchvision.datasets.CIFAR10(",/dataset",train=True,download=True,transform=torchvision.transforms.ToTensor())
test_data = torchvision.datasets.CIFAR10(",/dataset",train=False,download=True,transform=torchvision.transforms.ToTensor())
train_data_size=len(train_data)
test_data_size=len(test_data)

print("训练数据集长度为：{}".format(train_data_size))
print("测试数据集长度为：{}".format(test_data_size))

#利用dataloader加载数据集

train_dataloader = DataLoader(train_data,batch_size=32)
test_dataloader = DataLoader(test_data,batch_size=32)

#搭建神经网络

class Lzr(nn.Module):
    def __init__(self):
        super(Lzr,self).__init__()
        self.model = nn.Sequential(
        Conv2d(3, 32, 5, padding=2),
        MaxPool2d(2),
        Conv2d(32, 32, 5, padding=2),
        MaxPool2d(2),
        Conv2d(32, 64, 5, padding=2),
        MaxPool2d(2),
        Flatten(),
        Linear(1024, 64),
        Linear(64, 10)
        )

    def forward(self, x):
        x = self.model(x)
        return x

lzr = Lzr()


#损失函数
loss_fn = nn.CrossEntropyLoss()

#优化器
learning_rate = 1e-2;
optimizer= torch.optim.SGD(lzr.parameters(),lr=learning_rate)

total_train_step = 0
total_test_step = 0

epoch = 10
writer = SummaryWriter("./logs_train")
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
        if total_train_step % 100 == 0:
            print("训练次数：{}，Loss：{}".format(total_train_step,loss.item()))
            writer.add_scalar("train_loss",loss.item(),total_train_step)

    #测试步骤
    total_test_loss= 0
    with torch.no_grad():
        for data in test_dataloader:
            imgs,targets = data
            outputs= lzr(imgs)
            loss = loss_fn(outputs,targets)
            total_test_loss = total_test_loss +loss.item()
    print("整体测试集的Loss：{}".format(total_test_loss))
    writer.add_scalar("test_loss", total_test_loss, total_test_step)
    total_test_step=total_test_step+1

    torch.save(lzr,"lzr_{}.pth".format(i))
    print("模型已保存")
writer.close()