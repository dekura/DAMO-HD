'''
Author: Guojin Chen @ CUHK-CSE
Homepage: https://dekura.github.io/
Date: 2021-02-05 17:27:11
LastEditTime: 2021-09-10 11:40:05
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
in_dir = '/research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/haoyu_data/ispdmc'
# in_dir = '/Users/dekura/Downloads/pngs/'
out_dir = '/research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/ispdhaoyu_gen_single/test'

in_dir = Path(in_dir)
out_dir = Path(out_dir)


for im in tqdm(list(sorted(in_dir.glob('*.png')))):
    im_name = im.name
    # print(im_name)
    # print(str(in_dir / im_name))
    im = Image.open(str(im)).convert('1')
    # im = Image.open(str(im)).convert('RGB')
    imA = im.crop((0, 0, 2000, 2000))
    imA = np.asarray(imA)
    imB = im.crop((2000, 0, 4000, 2000))
    imB = np.asarray(imB)
    imC = im.crop((4000, 0, 6000, 2000))
    # imC = np.asarray(imC)
    imA_np = np.asarray(imA)
    imB_np = np.asarray(imB)
    imAB = np.zeros_like(imA)
    imAB[np.where(imA >= 1)] = 1
    imAB[np.where(imB >= 1)] = 1
    imAB = Image.fromarray(imAB)
    border_wh = 24
    new_wh = 2048

    imAB_border = Image.new('1', (new_wh, new_wh))
    imAB_border.paste(imAB, (border_wh, border_wh))

    imC_border = Image.new('1', (new_wh, new_wh))
    imC_border.paste(imC, (border_wh, border_wh))

    imABC = np.concatenate([np.asarray(imAB_border), np.asarray(imC_border)], 1)
    imABC = Image.fromarray(imABC)

    out_p = out_dir / im_name
    imABC.save(str(out_p))


