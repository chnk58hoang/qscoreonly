from torchvision.models import resnet50
from iresnet import iresnet50
import torch.nn as nn
import torch
import pickle


class XFIQA(nn.Module):
    def __init__(self, weight_path=None):
        super().__init__()
        self.backbone = nn.Sequential(*list(iresnet50().children())[:5])
        self.backbone.load_state_dict(torch.load(weight_path),strict=False)
        self.medium = nn.LazyLinear(64)
        self.pose_classifier = nn.Sequential(*[nn.LazyLinear(32),nn.LazyLinear(2)])

    def forward(self, image):
        image = self.backbone(image)
        image = image.reshape(image.size(0), image.size(1), -1)
        image = self.medium(image)
        image = image.reshape(image.size(0), -1)
        pose = self.pose_classifier(image)
        return pose


image = torch.rand(1, 3, 112, 112)
model = XFIQA(weight_path='/home/artorias/PycharmProjects/MYFIQAC/181952backbone.pth')
x = model(image)
print(x.size())
