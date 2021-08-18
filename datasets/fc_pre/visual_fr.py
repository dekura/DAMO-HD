'''
@Author: Guojin Chen
@Date: 2020-04-12 16:57:37
LastEditTime: 2021-08-14 00:54:58
@Contact: cgjhaha@qq.com
@Description: visualize final rects
'''
import glob
import gdspy
import numpy as np
import sys
import os
import shelve
from tqdm import tqdm
from const import PRECISION, LAYERS, VIA_WH, MERGE_WH


VIA_LAYER = LAYERS['design']
OPC_LAYER = LAYERS['mask']
SRAF_LAYER = LAYERS['sraf']
MERGE_LAYER = LAYERS['dbscan']
FR_WIN_LAYER = LAYERS['final_win']


def poly_to_rect(poly):
    xl = poly[0][0]  # 25
    xr = poly[1][0]  # 75
    yd = poly[0][1]  # 25
    yu = poly[2][1]  # 75
    point1 = np.array([xl, yd])
    point2 = np.array([xr, yu])
    return (point1, point2)

def merge_rect_by_poly(poly):
    xl = poly[0][0]  # 25
    xr = poly[1][0]  # 75
    yd = poly[0][1]  # 25
    yu = poly[2][1]  # 75
    merge_margin = (MERGE_WH // 2 - VIA_WH // 2)/PRECISION
    point1 = np.array([xl-merge_margin, yd-merge_margin])
    point2 = np.array([xr+merge_margin, yu+merge_margin])
    return (point1, point2)


def center_by_poly(poly):
    xl = poly[0][0]  # 25
    xr = poly[1][0]  # 75
    yd = poly[0][1]  # 25
    yu = poly[2][1]  # 75
    x = (xl + xr)/2
    y = (yd + yu)/2
    center = np.array([x, y])
    return center

def scale_gds(gds_path, Outfolder, args):
    filename = os.path.basename(gds_path)
    GdsIn = gds_path
    gdsii   = gdspy.GdsLibrary()
    gdsii.read_gds(GdsIn,units='convert')
    cell    = gdsii.top_level()[0]
    dtype = 0  #Layout Data Type
    token = 1
    gds_name = os.path.basename(gds_path)
    frdb_name = gds_name.replace('.gds','_fr')
    frdb_path = os.path.join(args.frdb_folder, frdb_name)
    db = shelve.open(frdb_path)
    final_rects = db['final_rects']
    for fr in tqdm(final_rects):
        rect_points = fr.rect
        rect = gdspy.Rectangle(rect_points[0], rect_points[1], layer=FR_WIN_LAYER)
        cell.add(rect)
    filename = filename.replace('.gds', '_fr_vis.gds')
    outpath  = os.path.join(Outfolder,filename)
    gdsii.write_gds(outpath)
        # txtname = filename.replace('.gds', '_centers.txt')
        # outtxtpath  = os.path.join(Outfolder,txtname)
        # np.savetxt(outtxtpath, centers, fmt='%.5f', delimiter=' ')


def visual_fr(args):
    Infolder = args.in_folder
    Outfolder = args.vis_folder
    restr = os.path.join(Infolder, '*.gds')
    gds_list = glob.glob(restr)
    for gds in tqdm(gds_list):
        scale_gds(gds, Outfolder, args)