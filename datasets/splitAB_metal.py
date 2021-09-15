'''
Author: Guojin Chen @ CUHK-CSE
Homepage: https://dekura.github.io/
Date: 2021-02-05 17:27:11
LastEditTime: 2021-09-10 17:00:13
Contact: cgjhaha@qq.com
Description:
imamge [A+B+C] => A,B,C
And we need to add 24 pixel border to fomulate the image.
'''

import numpy as np
from PIL import Image
from numpy.core.defchararray import asarray
from tqdm import tqdm
from pathlib import Path

# in_dir = '/research/d2/xfyao/guojin/data/datasets/develset/pngs'
# in_dir = '/research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/haoyu_data/metal/artimc'
in_dir = '/research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/haoyu_data/metal/iccad13mc'
# in_dir = '/Users/dekura/Downloads/pngs/'
# out_dir = '/research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/haoyu_data/metal_dls/train'
out_dir = '/research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/haoyu_data/metal_dls/test'

in_dir = Path(in_dir)
out_dir = Path(out_dir)


for im in tqdm(list(sorted(in_dir.glob('*.png')))):
    im_name = im.name
    # print(im_name)
    # print(str(in_dir / im_name))
    im = Image.open(str(im)).convert('1')
    # im = Image.open(str(im)).convert('RGB')
    imA = im.crop((0, 0, 2000, 2000))
    # imA = np.asarray(imA)
    imB = im.crop((2000, 0, 4000, 2000))
    # imB = np.asarray(imB)
    # imC = np.asarray(imC)
    # imA_np = np.asarray(imA)
    # imB_np = np.asarray(imB)


    border_wh = 24
    new_wh = 2048

    imA_border = Image.new('1', (new_wh, new_wh))
    imA_border.paste(imA, (border_wh, border_wh))

    imB_border = Image.new('1', (new_wh, new_wh))
    imB_border.paste(imB, (border_wh, border_wh))

    imAB = np.concatenate([np.asarray(imA_border), np.asarray(imB_border)], 1)
    imAB = Image.fromarray(imAB)

    out_p = out_dir / im_name
    imAB.save(str(out_p))


