import cv2
import numpy as np
from PIL import Image

import os, sys, glob
from tqdm import tqdm

import torch
import torch.nn.functional as F

from innerverz import Data_Process
DP = Data_Process()

from innerverz import FaceAligner
FA = FaceAligner(512, align_style='ffhq')

from innerverz import DECA
deca = DECA()

from util import set_random_colors, plot_kpts

from main import LMK_Warping
g = LMK_Warping()

source_list = [
    'YEJI.png',
    'WINTER.png',
    'uc_388.png',
    'uc_648.png',
    'HYERI.jpg',
    'Jenny.jpg',
    '003652.png',
]
video_list = [
    'video_1',
    'video_3',
    'video_4',
    'video_5',
]

save_path = './results_original'

colors = set_random_colors()

from innerverz import FaceParser
FP = FaceParser()        

# source
for source_name in tqdm(source_list):
    source_path = os.path.join(f'./assets/images/{source_name}')
    to_image = cv2.imread(source_path)
    _, to_lmk, _ = FA.detect_lmk(to_image)
    to_face, to_tfm, _, _ = FA.align_face_from_106(to_image, to_lmk)
    align_to_lmk = FA.affine_transform(to_lmk, to_tfm)

    to_face_dict = deca.data_preprocess(to_face, align_to_lmk)
    to_code_dict = deca.encode(to_face_dict['image'][None,...])

    for video_name in tqdm(video_list):
        os.makedirs(f'{save_path}/{source_name[:-4]}_{video_name}', exist_ok=True)
        
        count = 0
        frame_paths = os.path.join(f'./assets/videos/{video_name}/*.*')
        for frame_path in sorted(glob.glob(frame_paths)):
            from_image = cv2.imread(frame_path)
            size = from_image.shape[:-1]
            
            _, from_lmk, _ = FA.detect_lmk(from_image)
            from_face, from_tfm, from_tfm_inv, _ = FA.align_face_from_106(from_image, from_lmk)
            align_from_lmk = FA.affine_transform(from_lmk, from_tfm)
            
            from_face_dict = deca.data_preprocess(from_face, align_from_lmk)
            from_code_dict = deca.encode(from_face_dict['image'][None,...])

            new_code_dict = from_code_dict.copy()
            new_code_dict['shape'] = to_code_dict['shape']

            from_vis_dict = deca.decode(from_code_dict, original_image=from_face_dict['original_image'][None, ...], tform=torch.inverse(from_face_dict['tform'][None, ...]).transpose(1,2))
            from_lmk_points = from_vis_dict['landmarks2d_points']

            new_vis_dict = deca.decode(new_code_dict, original_image=from_face_dict['original_image'][None, ...], tform=torch.inverse(from_face_dict['tform'][None, ...]).transpose(1,2))
            new_lmk_points = new_vis_dict['landmarks2d_points']
            
            # data pp
            from_lmks_vis = plot_kpts(np.zeros_like(from_face), from_lmk_points, colors)
            to_lmks_vis = plot_kpts(np.zeros_like(from_face), new_lmk_points, colors)
            ts_from_face = DP.image_pp(from_face, size=256, batch=True, device='cuda')
            ts_from_lmks_vis = DP.image_pp(from_lmks_vis, size=256, batch=True, device='cuda')
            ts_to_lmks_vis = DP.image_pp(to_lmks_vis, size=256, batch=True, device='cuda')
            
            result = g(ts_from_face, ts_from_lmks_vis, ts_to_lmks_vis)       
            _result = DP.vis_pp(F.interpolate(result,(512,512),mode='bilinear'), normalize=False) # 0 - 1 -> 0 ~ 255
            
            from_label = FP.get_label(F.interpolate(ts_from_face, (512,512)), 512)
            from_innerface_mask = torch.where(from_label < 14, 1, 0) - torch.where(from_label==0, 1, 0) - torch.where(from_label==7, 1, 0) - torch.where(from_label==8, 1, 0) - torch.where(from_label==9, 1, 0)
            _from_innerface_mask = from_innerface_mask.squeeze().cpu().numpy()
            _from_innerface_mask = DP.mask_pp(_from_innerface_mask*255, 5, 0, 15)[...,None] / 255
            
            _from_innerface_mask = cv2.warpAffine(_from_innerface_mask, from_tfm_inv, (size[1], size[0]))
            _result = cv2.warpAffine(_result, from_tfm_inv, (size[1], size[0]))
            
            bg_result = from_image * (1-_from_innerface_mask) + _result * _from_innerface_mask
            # grid = np.concatenate((to_face, from_lmks_vis * .5 + to_lmks_vis * .5, from_face * .5 + from_lmks_vis * .5, _result * .5 + to_lmks_vis * .5, from_face, _result, abs(from_face - _result), bg_result), axis=1)
            grid = np.concatenate((from_image, bg_result), axis=1)
            cv2.imwrite(f'{save_path}/{source_name[:-4]}_{video_name}/{str(count).zfill(6)}.png', grid)
            count += 1
            
        os.system(f'ffmpeg -f image2 -i {save_path}/{source_name[:-4]}_{video_name}/%06d.png -vb 20M -pix_fmt yuv420p -src_range 1 -dst_range 1 {save_path}/{source_name[:-4]}_{video_name}.mp4')