import cv2
import torch.nn.functional as F

from innerverz import Data_Process
from torchvision.transforms.functional import to_tensor, rgb_to_grayscale

image_path = 'sample1.png'
DP = Data_Process()

"""
        face alignment usage
"""
from innerverz import FaceAligner
FA = FaceAligner(align_style='ffhq')

cv2_image = cv2.imread(image_path)
return_dict = FA.get_face(cv2_image)
aligned_face, tfm, tfm_inv, lms_106, face_bool = return_dict['face_img'], return_dict['tfm'], return_dict['tfm_inv'], return_dict['lms_106'], return_dict['facebool']

aligned_lmks_106 = FA.affine_transform(lms_106, tfm)['transform_lms_106']

"""
        DECA usage
"""
from innerverz import DECA
deca = DECA()
image_dict = deca.data_preprocess(aligned_face, aligned_lmks_106)
code_dict, vis_dict = deca(image_dict)

inputs = DP.vis_pp(vis_dict['inputs'], normalize=False)
landmarks2d = DP.vis_pp(vis_dict['landmarks2d'], normalize=False)
landmarks3d = DP.vis_pp(vis_dict['landmarks3d'], normalize=False)
shape_images = DP.vis_pp(vis_dict['shape_images'], normalize=False)
shape_detail_images = DP.vis_pp(vis_dict['shape_detail_images'], normalize=False)

cv2.imwrite('tmp.png', shape_detail_images/2 + aligned_face/2)