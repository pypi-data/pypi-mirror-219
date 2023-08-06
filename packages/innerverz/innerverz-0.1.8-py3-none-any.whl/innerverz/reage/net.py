import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from .net_utils import ConvBlock, BlurPool
from collections import namedtuple

class Interpolate(nn.Module):
    def __init__(self, scale_factor, mode="bilinear"):
        super(Interpolate, self).__init__()
        self.interp = nn.functional.interpolate
        self.scale_factor = scale_factor
        self.mode = mode
        
    def forward(self, x):
        x = self.interp(x, scale_factor=self.scale_factor, mode=self.mode, align_corners=False)
        return x

class DownLayer(nn.Module):
    def __init__(self, input_nc=1024):
        super(DownLayer, self).__init__()
        
        # self.resize = Interpolate(.5)
        self.blurpool = BlurPool(input_nc)
        self.conv_1 = nn.Conv2d(input_nc, input_nc*2, 3, stride=1, padding=1)
        self.act1 = nn.LeakyReLU(0.2)
        self.conv_2 = nn.Conv2d(input_nc*2, input_nc*2, 3, stride=1, padding=1)
        self.act2 = nn.LeakyReLU(0.2)
        
        
    def forward(self, x):
        x = self.blurpool(x)
        x = self.conv_1(x)
        x = self.act1(x)
        x = self.conv_2(x)
        x = self.act2(x)
        return x
    
class UpLayer(nn.Module):
    def __init__(self, input_nc=1024):
        super(UpLayer, self).__init__()
        self.resize = Interpolate(2)
        self.blurpool = BlurPool(input_nc, stride=1)
        self.conv_1 = nn.Conv2d(input_nc + input_nc//2, input_nc//2, 3, stride=1, padding=1)
        self.act1 = nn.LeakyReLU(0.2)
        self.conv_2 = nn.Conv2d(input_nc//2, input_nc//2, 3, stride=1, padding=1)
        self.act2 = nn.LeakyReLU(0.2)
        
        
    def forward(self, x, skip):
        x = self.resize(x)
        x = self.blurpool(x)
        x = torch.cat((x, skip), dim=1)
        x = self.conv_1(x)
        x = self.act1(x)
        x = self.conv_2(x)
        x = self.act2(x)
        return x
        

class Unet(nn.Module):
    def __init__(self, input_nc=5, output_nc=3):
        super(Unet, self).__init__()
        
        self.conv_1 = nn.Conv2d(input_nc, 32, 3, stride=1, padding=1)
        self.act_1 = nn.LeakyReLU(0.2)
        self.conv_2 = nn.Conv2d(32, 32, 3, stride=1, padding=1)
        self.act_2 = nn.LeakyReLU(0.2)
        
        self.downlayer1 = DownLayer(32)
        self.downlayer2 = DownLayer(64)
        self.downlayer3 = DownLayer(128)
        self.downlayer4 = DownLayer(256)
        
        self.uplayer1 = UpLayer(512)
        self.uplayer2 = UpLayer(256)
        self.uplayer3 = UpLayer(128)
        self.uplayer4 = UpLayer(64)
        
        self.output_layer = nn.Conv2d(32, output_nc, 1, stride=1, padding=0)

    def forward(self, x):
        x1 = self.conv_1(x)
        x2 = self.act_1(x1) 
        x3 = self.conv_2(x2) 
        x4 = self.act_2(x3) 
        x5 = self.downlayer1(x4) 
        x6 = self.downlayer2(x5) 
        x7 = self.downlayer3(x6) 
        x8 = self.downlayer4(x7)   # -> 1024
        x9 = self.uplayer1(x8, x7)
        x10 = self.uplayer2(x9, x6)
        x11 = self.uplayer3(x10, x5)
        x12 = self.uplayer4(x11, x4)
        x13 = self.output_layer(x12)
        return x13

class MyGenerator(nn.Module):
    def __init__(self):
        super(MyGenerator, self).__init__()
        self.generator = Unet()
        
    def forward(self, inputs):
        return self.generator(inputs)

#     def set_dict(self, input):
#         self.net_dict = {}
#         self.net_dict["from_age_image"] = input[0]
#         self.net_dict["model_input"] = input[1]
        

#     def forward(self, input):
#         self.set_dict(input)

#         self.net_dict['aging_delta'] = self.generator(self.net_dict["model_input"])
#         self.net_dict['fake'] = self.net_dict["from_age_image"] + self.net_dict['aging_delta']

#         return self.net_dict['fake'], self.net_dict['aging_delta']
