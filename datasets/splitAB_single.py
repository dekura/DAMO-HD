'''
Author: Guojin Chen @ CUHK-CSE
Homepage: https://dekura.github.io/
Date: 2021-02-05 17:27:11
LastEditTime: 2021-08-30 18:52:54
Contact: cgjhaha@qq.com
Description:
imamge [A+B] => A,B
'''

import numpy as np
from PIL import Image
from tqdm import tqdm
from pathlib import Path

# in_dir = '/research/d2/xfyao/guojin/data/datasets/develset/pngs'
in_dir = '/research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/maskg_contourw_rect_paired_rgb_2048/combine_AB/train'
# in_dir = '/Users/dekura/Downloads/pngs/'
out_dir = '/research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/maskg_contourw_rect_unpaired_single_2048'

in_dir = Path(in_dir)
out_dir = Path(out_dir)

out_A = out_dir / 'train_A'
out_B = out_dir / 'train_B'

out_A.mkdir(exist_ok=True)
out_B.mkdir(exist_ok=True)

for im in tqdm(list(sorted(in_dir.glob('*.png')))):
    im_name = im.name
    print(im_name)
    print(str(out_A / im_name))
    im = Image.open(str(im)).convert('1')
    # im = Image.open(str(im)).convert('RGB')
    imA = im.crop((0, 0, 2048, 2048))
    imB = im.crop((2048, 0, 4096, 2048))
    imA.save(str(out_A / im_name))
    imB.save(str(out_B / im_name))


