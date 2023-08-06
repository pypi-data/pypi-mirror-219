import os
import sys

import torch
import torch.nn as nn

from .net import MyGenerator
from ..utils import check_ckpt_exist, get_url_id

class Reage(nn.Module):
    def __init__(self, folder_name='reage', ckpt_name = 'G_512_130k.pt', force=False, device = 'cuda'):
        """
        Related Links
        --------
        https://studios.disneyresearch.com/2022/11/30/production-ready-face-re-aging-for-visual-effects/
        
        Options
        --------
        ckpt_name
            - G_512_130k.pt : image size(512)
            - G_1024_110k.pt : image size(1024)
        
        Forwards
        --------
        input
            - face image
                - aligned face with ffhq rules
                - dtype : tensor
                - shape : (b, 3, h, w)
                - min max : (-1 1)
            
            - mask 
                - skin(1) + brow(2,3) + ears(7,8) + nose(10) + mouth(11) + lip(12,13) + neck(14) area
                - dtype : tensor
                - shape : (b, 1, h, w)
                - min max : (0 or 1)
            - from_age, to_age
                - dtype : int
                - min max : (20 ~ 80)
            
        output
            dicts
            'result'
                - dtype : tensor
                - shape : (b, 3, h, w)
                - min max : (-1 1)
            'delta'
                - dtype : tensor
                - shape : (b, 3, h, w)
                - min max : (-1 1)
            
        """
        super(Reage, self).__init__()
        self.device = device
        self.generator = MyGenerator().to(self.device)
        
        url_id = get_url_id('~/.invz_pack/', folder_name, ckpt_name)
        root = os.path.join('~/.invz_pack/', folder_name)
        ckpt_path = check_ckpt_exist(root, ckpt_name = ckpt_name, url_id = url_id, force = force)
        ckpt = torch.load(ckpt_path, map_location=self.device)

        self.generator.load_state_dict(ckpt['model'])
        for param in self.generator.parameters():
            param.requires_grad = False
        self.generator.eval()
        del ckpt
        
    def forward(self, masked_image, mask, from_age, to_age, dicts={}) -> dict:
        
        model_input = torch.cat((masked_image, mask * from_age / 100, mask * to_age / 100), dim=1)
        
        delta = self.generator(model_input)
        result = masked_image + delta
        
        
        dicts['image'] = masked_image
        dicts['mask'] = mask
        dicts['from_age'] = from_age
        dicts['to_age'] = to_age
        dicts['result'] = result
        dicts['delta'] = delta
        return  dicts