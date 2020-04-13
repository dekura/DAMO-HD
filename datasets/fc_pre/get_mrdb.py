'''
@Author: Guojin Chen
@Date: 2020-04-12 09:07:45
@LastEditTime: 2020-04-13 14:55:10
@Contact: cgjhaha@qq.com
@Description: stat the merge_out.gds
'''

'''
TODO:
    store the via (x, y)
    store the merge_rect
'''

import glob
import gdspy
import shelve
import numpy as np
import sys
import os
from tqdm import tqdm
from shapes import MERGE_RECT
from const import LAYERS, PRECISION, MERGE_WH, VIA_WH


VIA_LAYER = LAYERS['design']
OPC_LAYER = LAYERS['mask']
SRAF_LAYER = LAYERS['sraf']
MERGE_LAYER = LAYERS['dbscan']
MR_VIA_LAYER = 900


def center_to_rect(center):
    xl = center[0] - 20/PRECISION
    xr = center[0] + 20/PRECISION
    yd = center[1] - 20/PRECISION
    yu = center[1] + 20/PRECISION
    point1 = np.array([xl, yd])
    point2 = np.array([xr, yu])
    return (point1, point2)

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

def stat_gds(gds_path, Outfolder):
    filename = os.path.basename(gds_path)
    GdsIn = gds_path
    gdsii   = gdspy.GdsLibrary()
    lib_out = gdspy.GdsLibrary()

    gdsii.read_gds(GdsIn,units='convert')
    cell    = gdsii.top_level()[0]
    cell_out = lib_out.new_cell('TOP1', overwrite_duplicate=True)
    # cell_out = lib_out.top_level()[0]
    bbox    = cell.get_bounding_box()
    dtype = 0  #Layout Data Type

    viapolys = cell.get_polygons(by_spec=True)[(VIA_LAYER,dtype)]
    via_centers = np.zeros((len(viapolys), 2))
    for via_index,via_poly in tqdm(enumerate(viapolys)):
        center = center_by_poly(via_poly)
        via_centers[via_index] = center
        rect_points = poly_to_rect(via_poly)
        rect = gdspy.Rectangle(rect_points[0], rect_points[1], layer=VIA_LAYER)
        cell_out.add(rect)

    sellayer  = [MERGE_LAYER]
    token = 1
    merge_rects  = []
    for i in tqdm(range(len(sellayer))):
        try:
            polyset = cell.get_polygons(by_spec=True)[(sellayer[i],dtype)]
        except:
            token=0
            print("Layer not found, skipping...")
            break
        for poly in tqdm(polyset):
            mr = MERGE_RECT(poly)
            merge_rects.append(mr)
            mr.get_vias(via_centers)
            mr_rect = gdspy.Rectangle(mr.rect[0], mr.rect[1], layer=MERGE_LAYER)
            cell_out.add(mr_rect)
            for via_c in mr.vias:
                rect_points = center_to_rect(via_c)
                rect = gdspy.Rectangle(rect_points[0], rect_points[1], layer=MR_VIA_LAYER)
                cell_out.add(rect)
            # print(len(mr.vias))


    if token == 1:
        filename = filename.replace('.gds', '_stat.gds')
        outpath  = os.path.join(Outfolder,filename)
        lib_out.write_gds(outpath)
        db_name = filename.replace('.gds', '_mr')
        db_path = os.path.join(Outfolder, db_name)
        db = shelve.open(db_path)
        db['merge_rects'] = merge_rects
        db.close()
        # txtname = filename.replace('.gds', '_centers.txt')
        # outtxtpath  = os.path.join(Outfolder,txtname)
        # np.savetxt(outtxtpath, centers, fmt='%.5f', delimiter=' ')


def get_mrdb(args):
    Infolder = args.out_folder
    Outfolder = args.stat_folder
    restr = os.path.join(Infolder, '*.gds')
    gds_list = glob.glob(restr)
    for gds in tqdm(gds_list):
        stat_gds(gds, Outfolder)

# Infolder = sys.argv[1]
# Outfolder= sys.argv[2]
# dir = os.path.abspath(os.path.dirname(__file__))
# Infolder = os.path.join(dir,'input_gds')
# Infolder = '/Users/dekura/Downloads/ispd_in/'
# Outfolder = os.path.join(dir,'output_gds')





