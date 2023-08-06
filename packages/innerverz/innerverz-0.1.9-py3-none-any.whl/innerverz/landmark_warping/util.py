import random
import cv2
import numpy as np
from PIL import Image

# random color

def set_random_colors(num=68+3):
    colors = []
    cube_root = num
    for r in range(0, 255, int(255 / cube_root)):
        for g in range(0, 255, int(255 / cube_root)):
            for b in range(0, 255, int(255 / cube_root)):
                colors.append([int(r), int(g), int(b)])
    random.shuffle(colors)
    return colors
    
# ---------------------------------- visualization
# end_list = np.array([17, 21], dtype = np.int32) - 1
end_list = np.array([17, 22, 27, 42, 48, 31, 36, 68], dtype = np.int32) - 1
def plot_kpts(image, kpts, colors):
    ''' Draw 68 key points
    Args: 
        image: the input image
        kpt: (68, 2).
    '''
    image = image.copy()
    _kpts = kpts.copy()
    # kpts = kpts[:17]
    # kpts = np.concatenate((kpts[:17],kpts[27:36]), axis=0)
    
    for i, color in zip(range(_kpts.shape[0]-1), colors):
        st = _kpts[i, :2]
        if i in end_list:
            continue
        ed = _kpts[i + 1, :2]
        image = cv2.line(image, (int(st[0]), int(st[1])), (int(ed[0]), int(ed[1])), color, 1,  cv2.LINE_AA)

    image = cv2.line(image, (int(kpts[42-1][0]), int(kpts[42-1][1])), (int(kpts[37-1][0]), int(kpts[37-1][1])), colors[-3], 1,  cv2.LINE_AA)
    image = cv2.line(image, (int(kpts[48-1][0]), int(kpts[48-1][1])), (int(kpts[43-1][0]), int(kpts[43-1][1])), colors[-2], 1,  cv2.LINE_AA)
    image = cv2.line(image, (int(kpts[68-1][0]), int(kpts[68-1][1])), (int(kpts[61-1][0]), int(kpts[61-1][1])), colors[-1], 1,  cv2.LINE_AA)

    return image
