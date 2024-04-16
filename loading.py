import torchvision.transforms
from PIL import Image
from torch import nn
import torch
import torchvision
from torch import nn
from torch.nn import Conv2d, MaxPool2d, Flatten, Linear, Sequential
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

image_path = "./imgs/cute-puppy-dog-pet-face-hand-wallpaper-preview.jpg"
image= Image.open(image_path)
print(image)

Transform = torchvision.transforms.Compose([torchvision.transforms.Resize((32,32)),torchvision.transforms.ToTensor()])

image= Transform(image)

print(image.shape)


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

model = torch.load("lzr_0.pth")
print(model)
image = torch.reshape(image,(1,3,32,32))
model.eval()
with torch.no_grad():
    output = model(image)
print(output)
print(output.argmax(1))
