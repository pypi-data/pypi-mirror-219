
import os
import sys
import wandb
# sys.path.append('../')
# cwd = os.path.dirname(os.path.realpath(__file__))

import cv2
import numpy as np
from PIL import Image
import scipy
from skimage.io import imread
from skimage.transform import estimate_transform, warp, resize, rescale

import torch
import torch.nn as nn
import torch.nn.functional as F

import torchvision
import torchvision.transforms as transforms

# from .models.face_detectors import FAN
from .models.encoders import ResnetEncoder
from .models.FLAME import FLAME, FLAMETex
from .models.decoders import Generator

from .utils.util import copy_state_dict, batch_orth_proj, tensor_vis_landmarks, vertex_normals
from .utils.rotation_converter import batch_euler2axis
from .utils.tensor_cropper import transform_points
from .utils.renderer import SRenderY, set_rasterizer
from .utils import tracker_utils
from .utils.lmks_756 import indexes_756
from ..utils import check_ckpt_exist, convert_image_type, get_url_id

class DECA(nn.Module):
    def __init__(self, folder_name='deca', ckpt_name = 'ckpt.zip', force=False, device = 'cuda'):
        """
        Related Links
        --------
        DECA : https://github.com/yfeng95/DECA
        FLAME : https://github.com/Rubikplayer/flame-fitting
        
        Methods
        ---------
        - data_preprocess
        - encode
        - decode
        - forward
        """
        super(DECA, self).__init__()
        self.batch_orth_proj = batch_orth_proj
        self.tensor_vis_landmarks = tensor_vis_landmarks
        self.transform_points = transform_points
        url_id = get_url_id('~/.invz_pack/', folder_name, ckpt_name)
        root = os.path.join('~/.invz_pack/', folder_name)
        self.dir_folder_path = check_ckpt_exist(root, ckpt_name = ckpt_name, url_id = url_id, force = force)[:-4]

        self.use_tex = False
        
        self.device = device
        self.iscrop = True
        self.scale = 1.25
        self.resolution_inp = 224
        self.image_size = 224
        self.uv_size = 256
        self.rasterizer_type = 'pytorch3d' # 'standard'
        
        self._create_model()
        self._setup_renderer()
        
        self.indexes_756 = np.array(indexes_756, dtype=np.long)
        
    def _setup_renderer(self,):
        set_rasterizer(self.rasterizer_type)
        self.render = SRenderY(self.image_size, obj_filename=os.path.join(self.dir_folder_path, 'head_template.obj'), uv_size=self.uv_size, rasterizer_type=self.rasterizer_type).to(self.device)
        # face mask for rendering details
        mask = imread(os.path.join(self.dir_folder_path, 'uv_face_eye_mask.png')).astype(np.float32)/255.; mask = torch.from_numpy(mask[:,:,0])[None,None,:,:].contiguous()
        self.uv_face_eye_mask = F.interpolate(mask, [self.uv_size, self.uv_size]).to(self.device)
        mask = imread(os.path.join(self.dir_folder_path, 'uv_face_mask.png')).astype(np.float32)/255.; mask = torch.from_numpy(mask[:,:,0])[None,None,:,:].contiguous()
        self.uv_face_mask = F.interpolate(mask, [self.uv_size, self.uv_size]).to(self.device)
        # displacement correction
        fixed_dis = np.load(os.path.join(self.dir_folder_path, 'fixed_displacement_256.npy'))
        self.fixed_uv_dis = torch.tensor(fixed_dis).float().to(self.device)
        # mean texture
        # mean_texture = imread(os.path.join(self.dir_folder_path, 'mean_texture.jpg')).astype(np.float32)/255.; mean_texture = torch.from_numpy(mean_texture.transpose(2,0,1))[None,:,:,:].contiguous()
        # self.mean_texture = F.interpolate(mean_texture, [self.uv_size, self.uv_size]).to(self.device)
        # dense mesh template, for save detail mesh
        # self.dense_template = np.load(os.path.join(self.dir_folder_path, 'texture_data_256.npy'), allow_pickle=True, encoding='latin1').item()
    
    def _bbox2point(self, left, right, top, bottom, type='bbox'):
        ''' bbox from detector and landmarks are different
        '''
        if type=='kpt68':
            old_size = (right - left + bottom - top)/2*1.1
            center = np.array([right - (right - left) / 2.0, bottom - (bottom - top) / 2.0 ])
        elif type=='bbox':
            old_size = (right - left + bottom - top)/2
            center = np.array([right - (right - left) / 2.0, bottom - (bottom - top) / 2.0  + old_size*0.12])
        else:
            raise NotImplementedError
        return old_size, center
     
    def _create_model(self):
        # set up parameters
        n_shape = 100; n_tex = 50; n_exp = 50; n_cam = 3; n_pose = 6; n_light = 27; n_detail = 128
        use_tex = True
        max_z = 0.01
        # jaw_type = 'aa'
        
        self.n_param = n_shape+n_tex+n_exp+n_pose+n_cam+n_light
        self.n_detail = n_detail
        self.n_cond = n_exp + 3 # exp + jaw pose
        
        # param_list = ['shape', 'tex', 'exp', 'pose', 'cam', 'light']
        self.num_list = [n_shape, n_tex, n_exp, n_pose, n_cam, n_light]
        self.param_dict = {
            'shape' : 100,
            'tex' : 50,
            'exp' : 50,
            'pose' : 6,
            'cam' : 3,
            'light' : 27
        }

        # encoders
        self.E_flame = ResnetEncoder(outsize=self.n_param).to(self.device) 
        self.E_detail = ResnetEncoder(outsize=self.n_detail).to(self.device)
        # decoders
        self.flame = FLAME(self.dir_folder_path).to(self.device)
        if use_tex:
            self.flametex = FLAMETex(self.dir_folder_path).to(self.device)
        self.D_detail = Generator(latent_dim=self.n_detail+self.n_cond, out_channels=1, out_scale=max_z, sample_mode = 'bilinear').to(self.device)
        
        # resume model
        model_path = os.path.join(self.dir_folder_path, 'deca_model.tar')
        if os.path.exists(model_path):
            print(f'trained model found. load {model_path}')
            checkpoint = torch.load(model_path, map_location=self.device)
            self.checkpoint = checkpoint
            copy_state_dict(self.E_flame.state_dict(), checkpoint['E_flame'])
            copy_state_dict(self.E_detail.state_dict(), checkpoint['E_detail'])
            copy_state_dict(self.D_detail.state_dict(), checkpoint['D_detail'])
        else:
            print(f'please check model path: {model_path}')
            # exit()
        # eval mode
        self.E_flame.eval()
        self.E_detail.eval()
        self.D_detail.eval()
        
    def _decompose_code(self, code, num_dict):
        ''' Convert a flattened parameter vector to a dictionary of parameters
        code_dict.keys() = ['shape', 'tex', 'exp', 'pose', 'cam', 'light']
        '''
        code_dict = {}
        start = 0
        for key in num_dict:
            end = start+int(num_dict[key])
            code_dict[key] = code[:, start:end]
            start = end
            if key == 'light':
                code_dict[key] = code_dict[key].reshape(code_dict[key].shape[0], 9, 3)
        return code_dict
    
    def _displacement2normal(self, uv_z, coarse_verts, coarse_normals):
        ''' Convert displacement map into detail normal map
        '''
        batch_size = uv_z.shape[0]
        uv_coarse_vertices = self.render.world2uv(coarse_verts).detach()
        uv_coarse_normals = self.render.world2uv(coarse_normals).detach()
    
        uv_z = uv_z*self.uv_face_eye_mask
        uv_detail_vertices = uv_coarse_vertices + uv_z*uv_coarse_normals + self.fixed_uv_dis[None,None,:,:]*uv_coarse_normals.detach()
        dense_vertices = uv_detail_vertices.permute(0,2,3,1).reshape([batch_size, -1, 3])
        uv_detail_normals = vertex_normals(dense_vertices, self.render.dense_faces.expand(batch_size, -1, -1))
        uv_detail_normals = uv_detail_normals.reshape([batch_size, uv_coarse_vertices.shape[2], uv_coarse_vertices.shape[3], 3]).permute(0,3,1,2)
        uv_detail_normals = uv_detail_normals*self.uv_face_eye_mask + uv_coarse_normals*(1.-self.uv_face_eye_mask)
        return uv_detail_normals
    
    def data_preprocess(self, image, lmk):
        # imagename = os.path.splitext(os.path.split(image_path)[-1])[0]
        # image = np.array(Image.open(image_path).convert('L'))[:, :, None].repeat(3, axis=2)
        """
        Input
        ---------
            - dtype : cv2 image, numpy array
            - shape : (h, w, 3)
            - min max : (0, 255)
            
        Output
        ---------
            - dtype : dict
                - image
                    - dtype : tensor
                    - shape : (3, 224, 224)
                    - min max : (0, 1)
                - tform
                    - dtype : tensor
                    - shape : (3, 3)
                - original_image
                    - dtype : tensor
                    - shape : (3, h, w)
                    - min max : (0, 1)
        """
        if len(image.shape) == 2:
            image = image[:,:,None].repeat(1,1,3)
        if len(image.shape) == 3 and image.shape[2] > 3:
            image = image[:,:,:3]
        
        h, w, _ = image.shape
        if self.iscrop:
            left = np.min(lmk[:,0]); right = np.max(lmk[:,0]); top = np.min(lmk[:,1]); bottom = np.max(lmk[:,1])
            bbox_type = 'kpt68'
            old_size, center = self._bbox2point(left, right, top, bottom, type=bbox_type)
                
            size = int(old_size*self.scale)
            src_pts = np.array([[center[0]-size/2, center[1]-size/2], [center[0] - size/2, center[1]+size/2], [center[0]+size/2, center[1]-size/2]])
        else:
            src_pts = np.array([[0, 0], [0, h-1], [w-1, 0]])
        
        DST_PTS = np.array([[0,0], [0,self.resolution_inp - 1], [self.resolution_inp - 1, 0]])
        tform = estimate_transform('similarity', src_pts, DST_PTS)
        
        image = image/255.

        dst_image = warp(image, tform.inverse, output_shape=(self.resolution_inp, self.resolution_inp))
        dst_image = dst_image.transpose(2,0,1)
        return {'image': torch.tensor(dst_image).float().to(self.device),
                'tform': torch.tensor(tform.params).float().to(self.device),
                'tform_inv': torch.inverse(torch.tensor(tform.params)[None, ...]).transpose(1,2)[0].float().to(self.device),
                'original_image': torch.tensor(image.transpose(2,0,1)).float().to(self.device),
                }
        
    def forward(self, image_dict):
        tensor_images = image_dict['image'][None,...]
        tform_invs = image_dict['tform_inv'][None,...]
        original_image = image_dict['original_image'][None, ...]
        
        codedict = self.encode(tensor_images)
        orig_visdict = self.decode(codedict, original_image=original_image, tform_invs=tform_invs)    
        orig_visdict['inputs'] = original_image   
        
        return codedict, orig_visdict

    def encode(self, images):
        """
        Input
        ---------
        - dtype : dict
            - image
                - dtype : tensor
                - shape : (3, 224, 224)
                - min max : (0, 1)
            - tform
                - dtype : tensor
                - shape : (3, 3)
            - original_image
                - dtype : tensor
                - shape : (3, h, w)
                - min max : (0, 1)

            
        Output
        ---------
        - dtype : dict
            - shape
                - shape : (b, 100)
            - tex
                - shape : (b, 50)
            - exp
                - shape : (b, 50)
            - pose
                - shape : (b, 6)
            - cam
                - shape : (b, 3)
            - light
                - shape : (b, 9, 3)
            - images
                - shape : (b, 3, 224, 224)
                - min max : (0, 1)
            - detail
                - shape : (b, 128)
        """
        
        with torch.no_grad():
            parameters = self.E_flame(images)
            detailcode = self.E_detail(images)
            
        codedict = self._decompose_code(parameters, self.param_dict)
        codedict['images'] = images
        codedict['detail'] = detailcode
        
        return codedict
    
    def decode(self, codedict, albedo=True, original_image=None, tform_invs=None):
        """
        Input
        ---------
        - dtype : dict
            - shape
                - shape : (b, 100)
            - tex
                - shape : (b, 50)
            - exp
                - shape : (b, 50)
            - pose
                - shape : (b, 6)
            - cam
                - shape : (b, 3)
            - light
                - shape : (b, 9, 3)
            - images
                - shape : (b, 3, 224, 224)
                - min max : (0, 1)
            - detail
                - shape : (b, 128)

        Output
        ---------
        - dtype : dict
            - inputs
                - dtype : tensor
                - shape : (b, 3, h, w)
                - min max : (0, 1)
                
            - landmarks2d
                - dtype : tensor
                - shape : (b, 3, h, w)
                - min max : (0, 1)
                
            - landmarks3d
                - dtype : tensor
                - shape : (b, 3, h, w)
                - min max : (0, 1)
                
            - landmarks2d_points
                - dtype : tensor
                - shape : (b, 68, 2)
                - min max : (0, h or w)
                
            - landmarks3d_points
                - dtype : tensor
                - shape : (b, 68, 2)
                - min max : (0, h or w)
                
            - shape_images
                - dtype : tensor
                - shape : (b, 3, h, w)
                - min max : (0, 1)
                
            - shape_detail_images
                - dtype : tensor
                - shape : (b, 3, h, w)
                - min max : (0, 1)
        """
        
        ## decode
        verts, landmarks2d, landmarks3d, trans_verts, trans_landmarks2d, trans_landmarks3d, trans_landmarks_756_3d = self.get_lmks_from_params(codedict, tform_invs=tform_invs)
        
        # rendering
        albedo = self.flametex(codedict['tex']) if albedo else torch.zeros([codedict['images'].shape[0], 3, self.uv_size, self.uv_size], device=codedict['images'].device) 
        ops = self.render(verts, trans_verts, albedo, lights= codedict['light'],h=original_image.shape[-2], w=original_image.shape[-1], background=None)
        
        # detail
        uv_z = self.D_detail(torch.cat([codedict['pose'][:,3:], codedict['exp'], codedict['detail']], dim=1))
        uv_detail_normals = self._displacement2normal(uv_z, verts, ops['normals'])

        # extract shape images
        shape_images, _, grid, alpha_images = self.render.render_shape(verts, trans_verts, lights= codedict['light'], h=original_image.shape[-2], w=original_image.shape[-1], images=None, return_grid=True)
        detail_normal_images = F.grid_sample(uv_detail_normals, grid, align_corners=False)*alpha_images
        shape_detail_images = self.render.render_shape(verts, trans_verts, lights= codedict['light'], detail_normal_images=detail_normal_images, h=original_image.shape[-2], w=original_image.shape[-1], images=None)
        
        vis_landmarks2d = tensor_vis_landmarks(original_image, landmarks2d)
        vis_landmarks3d = tensor_vis_landmarks(original_image, landmarks3d)
        vis_landmarks_756_3d = tensor_vis_landmarks(original_image, trans_landmarks_756_3d)

        visdict = {
            'inputs': original_image, 
            'landmarks2d': vis_landmarks2d,
            'landmarks3d': vis_landmarks3d,
            'landmarks756_3d': vis_landmarks_756_3d,
            'landmarks2d_points': trans_landmarks2d,
            'landmarks3d_points': trans_landmarks3d,
            'landmarks756_3d_points': trans_landmarks_756_3d,
            'shape_images': shape_images,
            'shape_detail_images': shape_detail_images,
        }
        return visdict

    def setup_tracker(self, deca_params, sparse_lmks, tform_invs, device='cuda'):
        self.device = device
        self.w_lmks_68 = 10000
        self.w_lmks_oval = 10000 ## chin lmk from face_alignment

        self.w_exp = 0.02
        self.w_shape = 0.0003
        self.w_tex = 0.04
        
        # self.cameras = PerspectiveCameras()
        self.num_images = sparse_lmks.size()[0]
        self.sparse_lmks = sparse_lmks
        self.tform_invs = tform_invs
        self.lmk_mask = ~(self.sparse_lmks.sum(2, keepdim=True) == 0)
        self.setup_params(deca_params)
        
    def setup_params(self, deca_params):
        
        with torch.no_grad():
            self.shape = nn.Parameter(deca_params['shape'].clone().detach().float().cuda())
            self.tex = nn.Parameter(deca_params['tex'].clone().detach().float().cuda())
            self.exp = nn.Parameter(deca_params['exp'].clone().detach().float().cuda())
            self.pose = nn.Parameter(deca_params['pose'].clone().detach().float().cuda())
            self.cam = nn.Parameter(deca_params['cam'].clone().detach().float().cuda())
            self.light = nn.Parameter(deca_params['light'].clone().detach().float().cuda())
        
        self.params_group = [
            {'params': [self.shape], 'lr': 0.025, 'name': ['shape']},
            # {'params': [self.tex], 'lr': 0.05, 'name': ['tex']},
            # {'params': [self.exp], 'lr': 0.025, 'name': ['exp']},
            # {'params': [self.pose], 'lr': 0.005, 'name': ['pose']},
            # {'params': [self.cam], 'lr': 0.005, 'name': ['cam']},
            # {'params': [self.light], 'lr': 0.01, 'name': ['light']},
        ]

        self.params_optimizer = torch.optim.Adam(self.params_group)

    def optimize(self, aligned_faces, num_iter, target_name):
        
        for count in range(num_iter):
            verts, landmarks2d, landmarks3d, trans_verts, trans_landmarks2d, trans_landmarks3d = self.get_lmks_from_params({
                'shape': self.params_group[0]['params'][0].mean(0).expand(self.num_images, 100),
                # 'tex': self.params_group[1]['params'][0],
                # 'exp': self.params_group[2]['params'][0],
                # 'pose': self.params_group[3]['params'][0],
                # 'cam': self.params_group[4]['params'][0],
                # 'light': self.params_group[5]['params'][0],
                'tex': self.tex,
                'exp': self.exp,
                'pose': self.pose,
                'cam': self.cam,
                'light': self.light,
                })

            # loss
            loss = 0  
            loss += tracker_utils.oval_lmk_loss(trans_landmarks2d, self.sparse_lmks, self.lmk_mask) * self.w_lmks_oval # lmk_oval
            loss += tracker_utils.lmk_loss(trans_landmarks2d, self.sparse_lmks, self.lmk_mask) * self.w_lmks_68 # lmk_68
            loss1 = 0  
            loss1 += tracker_utils.oval_lmk_loss(trans_landmarks2d, self.sparse_lmks, self.lmk_mask) * self.w_lmks_oval # lmk_oval
            loss1 += tracker_utils.lmk_loss(trans_landmarks2d, self.sparse_lmks, self.lmk_mask) * self.w_lmks_68 # lmk_68
            
            # Reguralizers
            # loss += torch.sum(self.exp ** 2) * self.w_exp # exp
            loss += torch.sum((self.shape) ** 2) * self.w_shape # shape
            # loss += torch.sum((self.shape - self.shape) ** 2) * self.w_shape # shape
            # loss += torch.sum(self.tex ** 2) * self.w_tex # tex

            self.params_optimizer.zero_grad()
            loss.backward()
            self.params_optimizer.step()
            self.params_group[0]['params'][0] = nn.Parameter(self.params_group[0]['params'][0].mean(0).expand(self.num_images, 100).clone().detach())
                
            # self.params_group = [
            #     {'params': [self.shape], 'lr': 0.025, 'name': ['shape']},
            #     # {'params': [self.tex], 'lr': 0.05, 'name': ['tex']},
            #     # {'params': [self.exp], 'lr': 0.025, 'name': ['exp']},
            #     # {'params': [self.pose], 'lr': 0.005, 'name': ['pose']},
            #     # {'params': [self.cam], 'lr': 0.005, 'name': ['cam']},
            #     # {'params': [self.light], 'lr': 0.01, 'name': ['light']},
            # ]

            # self.params_optimizer = torch.optim.Adam(self.params_group)
            # self.params_optimizer = torch.optim.Adam(self.params_group)
            
            
            # self.params_group[0]['params'][0] = self.params_group[0]['params'][0][0].expand(self.num_images, 100).clone().detach()
            # print(f'Loss for color >>> {count}th iter {loss.item():.4f}')
            # wandb.log({'loss': loss1.item(), 'shape': self.params_group[0]['params'][0].mean().item()})
            
            if count % 1 == 0:
                params = {'shape': self.params_group[0]['params'][0], 'tex': self.tex, 'exp': self.exp, 'pose': self.pose, 'cam': self.cam, 'light': self.light}
                lmks_2ds = self.get_lmks_from_params(params, tform_invs=self.tform_invs)[-2]
                
                lmk_images = []
                for idx, lmks_2d in enumerate(lmks_2ds):
                    aligned_face = aligned_faces[idx].copy()
                    
                    for i in range(len(lmks_2d)):
                        st = lmks_2d[i, :2]
                        aligned_face = cv2.circle(aligned_face,(int(st[0]), int(st[1])), 1, (255,0,0), 2)
                        st = self.sparse_lmks[idx, i, :2]
                        aligned_face = cv2.circle(aligned_face,(int(st[0]), int(st[1])), 1, (0,0,255), 2)
                    
                    lmk_images.append(aligned_face)
                cv2.imwrite(f'{target_name}_{str(count).zfill(3)}.png', np.concatenate(lmk_images, axis=1))
                                    
    def save_params(self, save_dir, shape_only=True):
        param_dict = {}
                    
        if shape_only:
            np.save(os.path.join(save_dir, 'opt_shape_param.npy'), self.params_group[0]['params'][0].clone().detach().cpu().numpy())
        
        else:
            # from deca: ['shape', 'tex', 'exp', 'pose', 'cam', 'light']
            param_dict['shape'] = self.shape.clone().detach().cpu().numpy()
            param_dict['tex'] = self.tex.clone().detach().cpu().numpy()
            param_dict['exp'] = self.exp.clone().detach().cpu().numpy()
            param_dict['pose'] = self.pose.clone().detach().cpu().numpy()
            param_dict['cam'] = self.cam.clone().detach().cpu().numpy()
            param_dict['light'] = self.light.clone().detach().cpu().numpy()

            np.save(os.path.join(save_dir, 'opt_params.npy'), param_dict)
        
    def get_lmks_from_params(self, params_dict, tform_invs=None):
        
        assert 'shape' in params_dict.keys()
        expression_params = params_dict['exp'] if 'exp' in params_dict.keys() else self.exp
        pose_params = params_dict['pose'] if 'pose' in params_dict.keys() else self.pose
        cam_params = params_dict['cam'] if 'cam' in params_dict.keys() else self.cam
        tform_invs = self.tform_invs if tform_invs is None else tform_invs
        
        # flame
        verts, landmarks2d, landmarks3d, landmarks_756_3d = self.flame(
            shape_params=params_dict['shape'], 
            expression_params=expression_params, 
            pose_params=pose_params,
            )
            
        # projection
        trans_verts = batch_orth_proj(verts, cam_params); trans_verts[:,:,1:] = -trans_verts[:,:,1:]
        trans_landmarks2d = batch_orth_proj(landmarks2d, cam_params)[:,:,:2]; trans_landmarks2d[:,:,1:] = -trans_landmarks2d[:,:,1:]; # trans_landmarks2d = trans_landmarks2d*256 + 256
        trans_landmarks3d = batch_orth_proj(landmarks3d, cam_params); trans_landmarks3d[:,:,1:] = -trans_landmarks3d[:,:,1:]; # trans_landmarks3d = trans_landmarks3d*256 + 256
        trans_landmarks_756_3d = batch_orth_proj(landmarks_756_3d, cam_params); trans_landmarks_756_3d[:,:,1:] = -trans_landmarks_756_3d[:,:,1:]; # trans_landmarks3d = trans_landmarks3d*256 + 256
        
        trans_verts = transform_points(trans_verts, tform_invs, [224, 224], [512, 512])
        trans_landmarks2d = transform_points(trans_landmarks2d, tform_invs, [224, 224], [512, 512])*512/2+512/2
        trans_landmarks3d = transform_points(trans_landmarks3d, tform_invs, [224, 224], [512, 512])*512/2+512/2
        trans_landmarks_756_3d = transform_points(trans_landmarks_756_3d, tform_invs, [224, 224], [512, 512])*512/2+512/2

        return verts, landmarks2d, landmarks3d, trans_verts, trans_landmarks2d, trans_landmarks3d, trans_landmarks_756_3d

    def get_dense_lmks(self):
        return 