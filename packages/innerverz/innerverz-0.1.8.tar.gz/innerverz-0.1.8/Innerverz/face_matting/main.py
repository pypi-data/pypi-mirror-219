import os
import sys
sys.path.append('../')
cwd = os.path.dirname(os.path.realpath(__file__))

import cv2
import numpy as np
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.functional as F

import torchvision.transforms as transforms

from .nets import Generator_MatteFormer, RAFT
from .nets.utils import InputPadder, warp, get_unknown_tensor_from_pred
from ..utils import check_ckpt_exist, get_url_id

# from utils.util import crop

class Face_Matting(nn.Module):
    def __init__(self, img_size : int = 512, window_size = 7, split_amount=4, folder_name='face_matting', \
                    matt_PATH = 'G_79k.pt', raft_path = 'raft-things.pth', force=False, device = 'cuda'):
        super(Face_Matting, self).__init__()
        
        self.device = device
        
        url_id = get_url_id('~/.invz_pack/', folder_name, matt_PATH)
        root = os.path.join('~/.invz_pack/', folder_name)
        self.matt_PATH = check_ckpt_exist(root, ckpt_name = matt_PATH, url_id = url_id, force = force)
        
        url_id = get_url_id('~/.invz_pack/', folder_name, raft_path)
        root = os.path.join('~/.invz_pack/', folder_name)
        self.raft_path = check_ckpt_exist(root, ckpt_name = raft_path, url_id = url_id, force = force)
        
        self.img_size = img_size
        self.window_size = window_size
        self.side_window = self.window_size//2
        self.split_amount = split_amount
        self.k = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        
        # self.wt = torch.exp(-(torch.arange(self.window_size).float()-self.side_window)**2/(2*((self.side_window+0.5)))).reshape(self.window_size,1,1,1)
        self.wt = torch.exp(-(torch.arange(self.window_size).float()-self.side_window)**2/(2*((self.side_window+0.5)**2))).reshape(self.window_size,1,1,1)
        
        self._model_setting(self.matt_PATH, self.raft_path)
        
        self.tf_color = transforms.Compose([
            transforms.Resize((self.img_size, self.img_size)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        self.kernel = np.ones((3, 3), np.uint8)
        
    def forward(self, image, trimap, dicts={}):
        preds = self.generator(image, trimap)
            
        alpha_pred_os1, alpha_pred_os4, alpha_pred_os8 = preds['alpha_os1'], preds['alpha_os4'], preds['alpha_os8']

        # refinement
        alpha_pred = alpha_pred_os8.clone().detach()
        weight_os4 = get_unknown_tensor_from_pred(alpha_pred, rand_width=30, train_mode=False)
        alpha_pred[weight_os4>0] = alpha_pred_os4[weight_os4>0]
        weight_os1 = get_unknown_tensor_from_pred(alpha_pred, rand_width=15, train_mode=False)
        alpha_pred[weight_os1>0] = alpha_pred_os1[weight_os1>0]

        alpha_pred = alpha_pred[0, 0, ...].data.cpu() * 255
        
        return alpha_pred
    
    def get_trimap(self, label, pad_size=32, dilate_iter=15, erode_iter=10):
        # skin area
        skin_mask = np.where(label < 14, 1, 0) - np.where(label == 7, 1, 0) - np.where(label == 8, 1, 0) - np.where(label == 9, 1, 0) - np.where(label == 0, 1, 0)
        pad_skin_mask = np.pad(skin_mask, ((pad_size,pad_size),(pad_size,pad_size)))

        pred_area = cv2.dilate(np.array(pad_skin_mask).astype(np.float64), self.k, iterations=dilate_iter)
        certain_area = cv2.erode(np.array(pad_skin_mask).astype(np.float64), self.k, iterations=erode_iter)
        
        padded_trimap = pred_area * (1-certain_area) + 2 * certain_area
        trimap = padded_trimap[pad_size:-pad_size,pad_size:-pad_size]
        # trimap = np.concatenate((trimap[:256,:], skin_mask[256:,:]*2), axis=0)
        _trimap = torch.from_numpy(trimap.astype(np.long))
        trimap_onehot = F.one_hot(_trimap, num_classes=3).permute(2, 0, 1).float().unsqueeze(0)
        
        return trimap_onehot
    
    def warping(self, image_chunks, label_chunks, flow_chunks):
        warp_label_chunks = []
        for image_chunk, label_chunk, flow_chunk in zip(image_chunks, label_chunks, flow_chunks):
            warp_label_chunk = []
            pad_image_chunk = self._get_pad_chunk(image_chunk)
            pad_label_chunk = self._get_pad_chunk(label_chunk)
            pad_flow_chunk = self._get_pad_chunk(flow_chunk)
            for index in range(self.side_window, len(pad_image_chunk)-self.side_window):
                images = torch.cat(pad_image_chunk[index-self.side_window:index+self.side_window+1], dim=0)
                labels = torch.cat(pad_label_chunk[index-self.side_window:index+self.side_window+1], dim=0)
                flows = torch.cat(pad_flow_chunk[index-self.side_window:index+self.side_window+1], dim=0)

                output, mask = warp(torch.cat((images, labels), dim=1), flows)

                aligned_Is = output[:,0:3].detach()
                aligned_Ps = output[:,3:].detach()
                _image = pad_image_chunk[index].repeat(2*self.side_window+1, 1, 1, 1)
            
                # the spatial weight
                ws = torch.exp(-((aligned_Is-_image)**2).mean(dim=1, keepdims=True)/(2*(0.2**2))) * mask[:,0:1]
                aligned_Ps[self.side_window] = labels[self.side_window].to(labels.device)
                # the weight between i and i shoud be 1.0
                ws[self.side_window,:,:,:] = 1.0
                weights = ws * self.wt # weights = w(j,i)
                weights = weights / weights.sum(dim=(0), keepdims=True)
                fused_Ps = (aligned_Ps * weights).sum(dim=0, keepdims=True)
                if (aligned_Ps * weights).sum(dim=0, keepdims=True).argmax(1).max() != 0:
                    fused_Ps = fused_Ps.argmax(1).squeeze()
                    fused_Ps = F.one_hot(fused_Ps, num_classes=fused_Ps.max()+1).permute(2, 0, 1).float().unsqueeze(0)
                warp_label_chunk.append(fused_Ps)
            warp_label_chunks.append(warp_label_chunk)
        return warp_label_chunks
            
    def get_flow(self, image_chunks):
        flow_chunks = []
        
        for image_chunk in image_chunks:
            flow_chunk = []
            pad_image_chunk = self._get_pad_chunk(image_chunk)
            for index in range(self.side_window, len(pad_image_chunk)-self.side_window):
                image2 = torch.cat(pad_image_chunk[index-self.side_window:index+self.side_window+1], dim=0).to(self.device)
                image1 = pad_image_chunk[index].repeat(2*self.side_window+1,1,1,1).to(self.device)
                padder = InputPadder(image1.shape)
                
                image1, image2 = padder.pad(image1, image2)
                with torch.no_grad():
                    _, flows_up = self.raft((image1+1)*255.0/2, (image2+1)*255.0/2, iters=20, test_mode=True)
                flow_up = flows_up[self.side_window:self.side_window+1].cpu()
                flow_chunk.append(flow_up)
            flow_chunks.append(flow_chunk)
        return flow_chunks
    
    def _get_chunk_list(self, lists, n):
        m = len(lists)//n + 1 if len(lists)%n != 0 else len(lists)//n
        return [lists[i:i+m] for i in range(0,len(lists),m)]
    
    def _get_pad_chunk(self, chunk):
        pad_chunk = chunk[1:self.side_window+1][::-1] + chunk + chunk[-self.side_window-1:-1][::-1]
        return pad_chunk
    
    def _model_setting(self, face_matting_ckpt_path, raft_ckpt_path):
        # face matting model setting
        self.generator = Generator_MatteFormer().to(self.device)
        ckpt = torch.load(os.path.join(cwd, face_matting_ckpt_path), map_location=self.device)
        self.generator.load_state_dict(ckpt['model'])
        for param in self.generator.parameters():
            param.requires_grad = False
        self.generator.eval()
        
        self.raft = torch.nn.DataParallel(RAFT())
        ckpt = torch.load(os.path.join(cwd, raft_ckpt_path), map_location=self.device)
        self.raft.load_state_dict(ckpt)
        self.raft = self.raft.module
        for param in self.raft.parameters():
            param.requires_grad = False
        self.raft.eval().to(self.device)
        del ckpt
        