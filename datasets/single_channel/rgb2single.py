'''
Author: Guojin Chen @ CUHK-CSE
Homepage: https://dekura.github.io/
Date: 2021-08-25 08:28:29
LastEditTime: 2021-08-30 19:29:28
Contact: cgjhaha@qq.com
Description: translate the rgb image to single channel images.
'''

import torch
import torchvision
from tqdm import tqdm
import numpy as np
from PIL import Image
from pathlib import Path


in_dir = '/research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/maskg_contourw_rect_unpaired_rgb_2048'
out_dir = '/research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/maskg_contourw_rect_unpaired_single_2048'

in_dir = Path(in_dir)
out_dir = Path(out_dir)


def rgb2binary(in_dir: Path, out_dir: Path):
    for x in in_dir.iterdir():
        x_name = x.name
        out_x = out_dir / x_name
        Path.mkdir(out_x, exist_ok=True)
        for img in tqdm(list(x.glob('*.png'))):
            img_name = img.name
            out_img = out_x / img_name
            p = Image.open(str(img)).convert('RGB')
            r = p.getchannel('R')
            g = p.getchannel('G')
            b = p.getchannel('B')
            r = np.asarray(r)
            r[np.where(r>1)] = 1
            g = np.asarray(g)
            g[np.where(g>1)] = 1
            b = np.asarray(b)
            b[np.where(b>1)] = 1
            x, y = r.shape
            out_p = np.zeros(r.shape)
            out_p[np.where(r == 1)] = 1
            out_p[np.where(g == 1)] = 1
            out_p[np.where(b == 1)] = 1
            out_p = out_p*255
            out_p = Image.fromarray(out_p).convert('1')
            out_p.save(str(out_img))




if __name__ == '__main__':
    rgb2binary(in_dir, out_dir)
