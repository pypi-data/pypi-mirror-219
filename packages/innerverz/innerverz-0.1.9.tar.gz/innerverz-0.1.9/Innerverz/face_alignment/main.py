import os
import cv2
import numpy as np
from .retina_face import RetinaFace
from .landmark import Landmark
from .graphic_utils import *

class FaceAligner():
    def __init__(self, size = 1024, align_style = 'invz'):
        '''
        align_style has 2 options  
        
        "ffhq" : algorithm used in FFHQ dataset  
        
        "invz" : algorithm costumed by Innerverz.co    
        
        Methods
        --------
        - get_face
        - detect_lmk
        - detect_lmk_multi
        - align_face_from_106
        - affine_transform
        
        Return
        --------
        dicts
        '''
        
        self.backbone = RetinaFace()
        self.lmk_detector = Landmark()
        self.size = size
        self.align_style = align_style
        if self.align_style == 'ffhq':
            self.index_5 = [38,88,86,52,61]
        else:
            self.index_5 = None
            
        # self.dicts = {
        #     'img' : None,
        #     'face_img' : None,
        #     'lmks_106' : None,
        #     'tfm' : None,
        #     'tfm_inv' : None,
        #     'quad' : None,
        #     'transform_lmks_106' : None,
        #     'facebool': None,
        # }
        
    
    def get_face(self, img, pad=256, box_scale=None):
        """
        Input
        ---------
            - dtype : cv2 image
            - shape : (h, w, 3)
            - min max : (0, 255)
            
        Output
        ---------
            - aligned_face
                - dtype : numpy array
                - shape : (size, size, 3)
            - tfm
                - dtype : numpy array
                - shape : (2, 3)
            - tfm_inv
                - dtype : numpy array
                - shape : (2, 3)
            - lmks_106
                - dtype : numpy array
                - shape : (106, 2)
            - FaceBool
                - dtype : Bool
        """
                
        #get bounding box and confidence score from retina face
        result_dict = self.detect_lmk(img, pad)
        if result_dict['facebool']: 
            result_dict = self.align_face_from_106(img, result_dict['lmks_106'], box_scale=box_scale)
            return result_dict
    
        else :
            return result_dict
    
    def detect_lmk(self, img, pad=256, dicts={}):
        """
        Input
        ---------
            - dtype : cv2 image
            - shape : (h, w, 3)
            - min max : (0, 255)
            - pad[int]
            
        Output
        ---------
            - FaceBool
                - dtype : Bool
            - lmks_106
                - dtype : numpy array
                - shape : (106, 2)
        """
        
        pad_img = np.pad(img, ((pad, pad), (pad,pad), (0,0))) 
        temp, _ = self.backbone.detect(pad_img)
        
        if len(temp):
            bbox = temp[0][0:4]
            pad_lmks_106 = self.lmk_detector.get(pad_img, bbox)
            lmks_106 = pad_lmks_106 - pad
            dicts['lmks_106'] = lmks_106
            dicts['facebool'] = True
            return dicts

        else:
            dicts['lmks_106'] = None
            dicts['facebool'] = False
            return dicts
            
    def align_face_from_106(self, img, lmks_106, size=None, box_scale=None, dicts={}):
        """
        Input
        ---------
            - img
                - dtype : cv2 image
                - shape : (h, w, 3)
                - min max : (0, 255)
            - lmks_106
                - dtype : numpy array
                - shape : (106, 2)
            - size
                - dtype : int
            
        Output
        ---------
            - img
                - dtype : numpy array
                - shape : (size, size, 3)
            - facebool
                - dtype : numpy array
                - shape : (1)
            - lmks_106
                - dtype : numpy array
                - shape : (106, 2)
            - aligned_face
                - dtype : numpy array
                - shape : (size, size, 3)
            - aligned_lmks_106
                - dtype : numpy array
                - shape : (106, 2)
            - tfm
                - dtype : numpy array
                - shape : (2, 3)
            - tfm_inv
                - dtype : numpy array
                - shape : (2, 3)
            - quad
                - dtype : numpy array
                - shape : (4, 2)
            
        """
        if size is None: size = self.size
        
        if box_scale is None:
            box_scale = (2.0, 1.8) if self.align_style == 'ffhq' else (2.0, 4.0)
        
        if self.align_style == 'ffhq':
            # 5 points: [38, 88, 86, 52, 61]
            eye_left     = lmks_106[38]
            eye_right    = lmks_106[88]
            eye_avg      = (eye_left + eye_right) * 0.5
            eye_to_eye   = eye_right - eye_left
            mouth_left   = lmks_106[52]
            mouth_right  = lmks_106[61]
            mouth_avg    = (mouth_left + mouth_right) * 0.5
            eye_to_mouth = mouth_avg - eye_avg
            c = eye_avg + eye_to_mouth * 0.1
            
            ##################################################################################################
            x = eye_to_eye - np.flipud(eye_to_mouth) * [-1, 1]
            x /= np.hypot(*x) #x를 단위벡터로 만듦
            x *= max(np.hypot(*eye_to_eye) * box_scale[0], np.hypot(*eye_to_mouth) * box_scale[1])
            y = np.flipud(x) * [-1, 1] 
            ##################################################################################################
              
        elif self.align_style == 'invz':   
            eye_left     = (lmks_106[39] + lmks_106[35])*0.5
            eye_right    = (lmks_106[89] + lmks_106[93])*0.5
            eye_avg      = (eye_left + eye_right) * 0.5
            eye_to_eye   = eye_right - eye_left
            mouth_avg = (lmks_106[76] + lmks_106[82])*0.5
            eye_to_mouth = (mouth_avg - eye_avg)
            c = lmks_106[73]

            ##################################################################################################
            x = eye_to_eye.copy()
            x /= np.hypot(*x) #x를 단위벡터로 만듦
            x *= max(np.hypot(*eye_to_eye) * box_scale[0], np.hypot(*eye_to_mouth) * box_scale[1])
            y = np.flipud(x) * [-1, 1] 
            ##################################################################################################    
            
        quad = np.stack([c - x - y, c - x + y, c + x + y, c + x - y])
        src_pts = quad + 0.01*np.random.rand(4,2)
        ref_pts = np.array(((0, 0), (0, size), (size, size), (size, 0)))
        tfm, tfm_inv = get_similarity_transform_for_cv2(src_pts, ref_pts)
        aligned_face = cv2.warpAffine(np.array(img), tfm, (size, size), borderMode=None)
        # aligned_face = cv2.warpAffine(np.array(img), tfm, (size, size), borderMode=cv2.BORDER_REFLECT)
        aligned_lmks_106 = self.transform_lmks(lmks_106, tfm)['aligned_lmks_106']
        
        dicts['img'] = img
        dicts['facebool'] = True
        dicts['lmks_106'] = lmks_106
        dicts['box_scale'] = box_scale
        dicts['aligned_face'] = aligned_face
        dicts['aligned_lmks_106'] = aligned_lmks_106
        dicts['tfm'] = tfm
        dicts['tfm_inv'] = tfm_inv
        dicts['quad'] = quad
        return dicts
     
    def transform_lmks(self, lmks_106, tfm, dicts={}):
        """
        Input
        ---------
            - lmks_106
                - dtype : numpy array
                - shape : (106, 2)
            - tfm
                - dtype : numpy array
                - shape : (2, 3)
                
        Output
        ---------
            - dtype : numpy array
            - shape : (106, 2)
        """
        constant_term = np.ones((lmks_106.shape[0],1))
        expanded_points = np.concatenate((lmks_106, constant_term), axis=-1)
        result = np.matmul(expanded_points, np.transpose(tfm))
        dicts['aligned_lmks_106'] = result
        return dicts
    
    
    def detect_lmk_multi(self, img, pad=256, dicts={}):
        """
        Input
        ---------
            - dtype : cv2 image
            - shape : (h, w, 3)
            - min max : (0, 255)
            - pad[int]
            
        Output
        ---------
            - FaceBool
                - dtype : Bool
            - lmks_106
                - dtype : numpy array
                - shape : (106, 2)
        """
        
        pad_img = np.pad(img, ((pad, pad), (pad,pad), (0,0))) 
        temp, _ = self.backbone.detect(pad_img)
        
        if len(temp):
            lmks_106_list, facebool_list = [], []
            for i in range(len(temp)):
                bbox = temp[i][0:4]
                pad_lmks_106 = self.lmk_detector.get(pad_img, bbox)
                lmks_106 = pad_lmks_106 - pad
                lmks_106_list.append(lmks_106); facebool_list.append(True)
            dicts['lmks_106'] = lmks_106_list
            dicts['facebool'] = facebool_list
            return dicts

        else:
            dicts['lmks_106'] = None
            dicts['facebool'] = False
            return dicts