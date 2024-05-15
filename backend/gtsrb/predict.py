from PIL import Image
from torchvision.utils import save_image
from torchvision import transforms
import torchvision
import torch
import numpy as np

traffic_signs = [
    "Speed limit (20km/h)",
    "Speed limit (30km/h)",
    "Speed limit (50km/h)",
    "Speed limit (60km/h)",
    "Speed limit (70km/h)",
    "Speed limit (80km/h)",
    "End of speed limit (80km/h)",
    "Speed limit (100km/h)",
    "Speed limit (120km/h)",
    "No passing",
    "No passing for vehicles over 3.5 metric tons",
    "Right-of-way at the next intersection",
    "Priority road",
    "Yield",
    "Stop",
    "No vehicles",
    "Vehicles over 3.5 metric tons prohibited",
    "No entry",
    "General caution",
    "Dangerous curve to the left",
    "Dangerous curve to the right",
    "Double curve",
    "Bumpy road",
    "Slippery road",
    "Road narrows on the right",
    "Road work",
    "Traffic signals",
    "Pedestrians",
    "Children crossing",
    "Bicycles crossing",
    "Beware of ice/snow",
    "Wild animals crossing",
    "End of all speed and passing limits",
    "Turn right ahead",
    "Turn left ahead",
    "Ahead only",
    "Go straight or right",
    "Go straight or left",
    "Keep right",
    "Keep left",
    "Roundabout mandatory",
    "End of no passing",
    "End of no passing by vehicles over 3.5 metric tons"
]


def predict_from_file(img, module_filename: str) -> str:
    if type(img) == str:
        image = Image.open(img)
        to_tenser = transforms.Compose([transforms.ToTensor()])
        image = to_tenser(image)
    elif type(img) == np.ndarray:
        # print(img)
        to_tenser = transforms.Compose([transforms.ToTensor()])
        image = img[:, :, ::-1]
        image = Image.fromarray(image, mode="RGB")
        image = to_tenser(image)
    else:
        image = img

    if type(image) != torch.Tensor:
        raise ValueError(f'Error type of img, which should be a filepath(str), np.ndarray, or torch.Tensor. '
                         f'Got {type(image)}.')

    # TODO: 这个快变成狗屎了，先转成tenser存文件又读成PIL Image，看看能不能改。
    save_image(image, "temp_tensor.jpg")
    image = Image.open("temp_tensor.jpg")

    transform = torchvision.transforms.Compose(
        [torchvision.transforms.Resize((32, 32)),
         torchvision.transforms.ToTensor()
    ])

    # transform the image
    image = transform(image)
    # image = image.unsqueeze(0)  # Add a batch dimension
    image = torch.reshape(image, (1, 3, 32, 32))

    # 加载模型文件
    model = torch.load(module_filename)

    #关闭Dropout和BatchNorm等特性
    model.eval()

    # 预测
    with torch.no_grad():
        output = model(image)
    # print(output.argmax(1))
    predicted_indices = output.argmax(1)  # 获取每个样本预测类别的索引
    result = ""
    for index in predicted_indices:
        result = traffic_signs[index]
    print(result)
    return result
