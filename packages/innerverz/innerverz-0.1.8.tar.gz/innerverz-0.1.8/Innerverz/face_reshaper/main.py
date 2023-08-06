import os
import sys

import numpy as np
import torch
import torch.nn as nn

from .nets import MyGenerator
from .util import set_random_colors, plot_kpts, plot_kpt
from .vis_utils.vis_68 import contour_lines_68
from .vis_utils.vis_756 import contour_lines_756
from ..utils import check_ckpt_exist, get_url_id

class Face_Reshaper(nn.Module):
    def __init__(self, img_size : int = 512, color_num : int = 68, folder_name='face_reshaper', ckpt_name = 'G_38k_unalign_multiaug.pt', force=False, device = 'cuda'):
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
                    - shape : (68 2) or (756,2)
                    
                - size
                    - dtype : int
                    - default : 512
                    - plz check landmark size

                - color_nums
                    - dtype : int
                    - default : 68 or 756
            
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
        super(Face_Reshaper, self).__init__()
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
        
        if color_num == 68:
            self.contour_lines = np.array(contour_lines_68)
            self.colors = set_random_colors(num=color_num)
        elif color_num == 756:
            self.contour_lines = np.array(contour_lines_756)
            self.colors = set_random_colors(num=color_num)
        
    def get_vis_color_landmark(self, lmks, size=512, dicts={}) -> dict:
        canvas = np.zeros((size, size, 3))
        for (st, ed), color in zip(self.contour_lines, self.colors):
            st_point, ed_point = lmks[int(st)], lmks[int(ed)]
            canvas = plot_kpt(canvas, st_point, ed_point, color)
        dicts['vis_color_lmk'] = canvas
        return dicts

    def forward(self, from_face, from_color_vis_lmk, to_color_vis_lmk, dicts={}) -> dict:
        inputs = torch.cat((from_color_vis_lmk, to_color_vis_lmk), dim=1)
        result = self.generator(from_face, inputs)
        dicts['from_vis_lmks'] = from_color_vis_lmk
        dicts['to_vis_lmks'] = to_color_vis_lmk
        dicts['result'] = result
        return dicts
        