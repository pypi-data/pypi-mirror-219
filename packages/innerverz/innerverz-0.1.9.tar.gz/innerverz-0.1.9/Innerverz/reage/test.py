from innerverz import Reage
reage = Reage()

from innerverz import Data_Process
DP = Data_Process()

from innerverz import FaceParser
FP = FaceParser()

from innerverz import FaceAligner
FA = FaceAligner(512, 'ffhq')

import cv2
import numpy as np
from PIL import Image

import torch

image = cv2.imread('./assets/assets/000.png')
face,_,_,_,_,_ = FA.get_face(image)
ts_face = DP.image_pp(face, 512, normalize=True)
ts_label = FP.get_label(ts_face)
ts_label = ts_label.unsqueeze(0)
ts_mask = torch.where(ts_label<15, 1, 0)
ts_mask -= torch.where(ts_label==0, 1, 0)
ts_mask -= torch.where(ts_label==4, 1, 0)
ts_mask -= torch.where(ts_label==5, 1, 0)

result,_ = reage(ts_face, ts_mask, 40, 20)
vis_result = DP.vis_pp(result)
cv2.imwrite('./result.png', vis_result)