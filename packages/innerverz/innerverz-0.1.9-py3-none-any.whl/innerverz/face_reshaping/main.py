import os
import sys

import numpy as np
import torch
import torch.nn as nn

from .nets import MyGenerator
from .util import set_random_colors, plot_kpts
from ..utils import check_ckpt_exist, get_url_id

class Face_Reshaping(nn.Module):
    def __init__(self, img_size : int = 512, folder_name='face_reshaping', ckpt_name = 'G_38k_unalign_multiaug.pt', force=False, device = 'cuda'):
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
        super(Face_Reshaping, self).__init__()
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
        
        self.colors = set_random_colors(color_num=68+3)
        
    def get_vis_color_landmark(self, lmks, size=512, color_num=68+3, dicts={}) -> dict:
    # def get_vis_color_landmark(self, lmks, size=512, color_num=68+3):
        canvas = np.zeros((size, size, 3))
        vis_lmk = plot_kpts(canvas, lmks, self.colors)
        dicts['vis_color_lmk'] = vis_lmk
        return dicts

    def forward(self, from_face, from_color_vis_lmk, to_color_vis_lmk, dicts={}) -> dict:
        inputs = torch.cat((from_color_vis_lmk, to_color_vis_lmk), dim=1)
        result = self.generator(from_face, inputs)
        dicts['from_vis_lmks'] = from_color_vis_lmk
        dicts['to_vis_lmks'] = to_color_vis_lmk
        dicts['result'] = result
        return dicts
        