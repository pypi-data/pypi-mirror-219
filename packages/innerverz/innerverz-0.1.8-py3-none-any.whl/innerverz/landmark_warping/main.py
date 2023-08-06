import os
import sys

import numpy as np
import torch
import torch.nn as nn

from .util import set_random_colors, plot_kpts
from ..utils import check_ckpt_exist, get_url_id

class Landmark_Warping(nn.Module):
    def __init__(self, img_size : int = 512, folder_name='landmark_warping', ckpt_name = 'G_38k_unalign_multiaug.pt', force=False, device = 'cuda'):
        """
            Related Links
            --------
            https://meta-portrait.github.io/
            
            Options
            --------
            ckpt_name
                - G_13000.pt : image size(512)
            

            
            get_vis_color_landmark
            --------
            - input
                - lmks
                    - shape : (68 2)
                    
                - size
                    - dtype : int
                    - default : 512
                    - plz check landmark size

                - color_nums
                    - dtype : int
                    - default : 68 + 3
            
            - output
                - dicts 'vis_color_lmk'
                    - dtype : numpy
                    - shape : (3, h, w)
                    - min max : (0 255)
            
            Forwards
            --------
            - input
                - from face
                    - aligned face with ffhq rules
                    - dtype : tensor
                    - shape : (b, 3, h, w)
                    - min max : (-1 1)
                
                - from landmark vis
                    - dtype : tensor
                    - shape : (b, 3, h , w)
                    - min max : (-1 1)
                    
                - to landmark vis
                    - dtype : tensor
                    - shape : (b, 3, h , w)
                    - min max : (-1 1)
            - output
                - dicts 'result'
                    - dtype : tensor
                    - shape : (b, 3, h, w)
                    - min max : (-1 1)
                
        """
        super(Landmark_Warping, self).__init__()
        self.device = device
        self.img_size = img_size
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
        
        self.dicts = {}
        
    def get_vis_color_landmark(self, lmks, size=512, color_num=68+3):
        canvas = np.zeros_like((3, size, size))
        colors = set_random_colors(color_num)
        vis_lmk = plot_kpts(canvas, lmks, colors)
        self.dicts['vis_color_lmk'] = vis_lmk
        return self.dicts

    def forward(self, from_face, from_color_vis_lmk, to_color_vis_lmk):
        inputs = torch.cat((from_color_vis_lmk, to_color_vis_lmk), dim=1)
        result = self.generator(from_face, inputs)
        self.dicts['result'] = result
        return self.dicts
        