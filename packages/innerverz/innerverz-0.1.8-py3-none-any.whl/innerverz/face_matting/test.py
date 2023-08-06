import cv2
import numpy as np
from PIL import Image

import os, sys, glob
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms

from innerverz import FaceParser
FP = FaceParser()

from innerverz import Data_Process
DP = Data_Process()

from main import Face_Matting
FM = Face_Matting()

#==================
# video
#==================

os.makedirs('./tests_around', exist_ok=True)

count = 0
image_list, label_list = [], []
for image_path in sorted(glob.glob('./unit_clip/*.*')):
    image = Image.open(image_path).resize((512,512))
    
    np_image = np.array(image)

    h, w = np_image.shape[:2]
    div_h, div_w = 4, 4
    pix_hs, pix_ws = range(0, h, h//div_h), range(0, w, w//div_w)

    ts_image = DP.image_pp(image, normalize=True)
    label = FP.get_label(ts_image)
    label = label.clone().detach().squeeze().cpu().numpy()
    
    image_list.append(ts_image.cpu())
    label_list.append(label)
    
# get tri map
trimap_list = []
for label in label_list:
    trimap = FM.get_trimap(label)
    trimap_list.append(trimap)

image_chunks = FM._get_chunk_list(image_list, FM.split_amount)  
trimap_chunks = FM._get_chunk_list(trimap_list, FM.split_amount)  
flow_chunks = FM.get_flow(image_chunks)

warp_trimap_chunks = FM.warping(image_chunks, trimap_chunks, flow_chunks)

# predit
pred_chunks = []
for image_chunk, warp_trimap_chunk in zip(image_chunks, warp_trimap_chunks):
    pred_chunk = []
    for image, warp_trimap in zip(image_chunk, warp_trimap_chunk):
        _image = image.cuda() * .5 + .5
        _warp_trimap = warp_trimap.cuda()
        pred = FM(_image, _warp_trimap)
        pred = pred[None,None, ...]
        pred_chunk.append(pred)
    pred_chunks.append(pred_chunk)
    
result_chunks = FM.warping(image_chunks, pred_chunks, flow_chunks)
    
# vis
count = 0
for image_chunk, trimap_chunk, warp_trimap_chunk, result_chunk in zip(image_chunks, trimap_chunks, warp_trimap_chunks, result_chunks):
    for image, trimap, warp_trimap, result in zip(image_chunk, trimap_chunk, warp_trimap_chunk, result_chunk):
        vis_image = DP.vis_pp(image)
        vis_trimap = trimap.argmax(1).squeeze().cpu().unsqueeze(-1).repeat(1,1,3).numpy()*127.5
        vis_warp_trimap = warp_trimap.argmax(1).squeeze().cpu().unsqueeze(-1).repeat(1,1,3).numpy()*127.5
        grid = np.concatenate([vis_image, vis_trimap, vis_warp_trimap, result.squeeze().cpu().numpy()[:,:,None].repeat(3,axis=-1)], axis=1)
        cv2.imwrite(f'./tests_around/{str(count).zfill(6)}.png', grid)
        count += 1


#==================
# image
#==================
image_path = './unit_clip/003675.png'
image = Image.open(image_path).resize((512,512))
np_image = np.array(image)

h, w = np_image.shape[:2]
div_h, div_w = 4, 4
pix_hs, pix_ws = range(0, h, h//div_h), range(0, w, w//div_w)

ts_image = DP.image_pp(image)
label = FP.get_label(ts_image)
label = label.clone().detach().squeeze().cpu().numpy()
trimap = FM.get_trimap(label).to(ts_image.device)
pred = FM(ts_image, trimap)
_pred = pred.squeeze().cpu().numpy()[:,:,None].repeat(3,axis=-1)
cv2.imwrite('./image_test.png',_pred)
