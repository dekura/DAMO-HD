'''
Author: Guojin Chen @ CUHK-CSE
Homepage: https://dekura.github.io/
Date: 2021-02-05 17:27:11
LastEditTime: 2021-08-30 19:02:05
Contact: cgjhaha@qq.com
Description:
imamge [A+B] => A,B
'''

import numpy as np
from PIL import Image
from tqdm import tqdm
from pathlib import Path

# in_dir = '/research/d2/xfyao/guojin/data/datasets/develset/pngs'
in_dir = '/research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/maskg_contourw_rect_paired_rgb_2048/combine_AB/test'
# in_dir = '/Users/dekura/Downloads/pngs/'
in_dir = Path(in_dir)

out_A = in_dir.parent / 'test_A'
out_B = in_dir.parent / 'test_B'

out_A.mkdir(exist_ok=True)
out_B.mkdir(exist_ok=True)

for im in tqdm(list(sorted(in_dir.glob('*.png')))):
    im_name = im.name
    print(im_name)
    print(str(out_A / im_name))
    # im = Image.open(str(im)).convert('L')
    im = Image.open(str(im)).convert('RGB')
    imA = im.crop((0, 0, 2048, 2048))
    imB = im.crop((2048, 0, 4096, 2048))
    imA.save(str(out_A / im_name))
    imB.save(str(out_B / im_name))


