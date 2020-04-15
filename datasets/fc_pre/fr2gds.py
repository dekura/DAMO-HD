'''
@Author: Guojin Chen
@Date: 2020-04-13 16:50:58
@LastEditTime: 2020-04-13 17:51:42
@Contact: cgjhaha@qq.com
@Description: translate the final rects to gds layout
'''
import os
import glob
import gdspy
import shelve
import numpy as np
from tqdm import tqdm
from const import LAYERS, GDS_WIN_WH, PRECISION

VIA_LAYER = LAYERS['design']
OPC_LAYER = LAYERS['mask']
SRAF_LAYER = LAYERS['sraf']
MERGE_LAYER = LAYERS['dbscan']

def remove_margin(fr_center, rects):
    left_margin = fr_center[0] - (GDS_WIN_WH/2)/PRECISION
    down_margin = fr_center[1] - (GDS_WIN_WH/2)/PRECISION
    for rect in rects:
        rect[0][0] -= left_margin
        rect[0][1] -= down_margin
        rect[1][0] -= left_margin
        rect[1][1] -= down_margin
    return rects

def tran_gds(gds, out_folder, args):
    filename = os.path.basename(gds)
    frdb_name = filename.replace('.gds','_fr')
    frdb_path = os.path.join(args.frdb_folder, frdb_name)
    db = shelve.open(frdb_path)
    final_rects = db['final_rects']
    for fr_index, fr in tqdm(enumerate(final_rects)):
        gdspy.current_library = gdspy.GdsLibrary()
        gdsii = gdspy.GdsLibrary()
        cell = gdsii.new_cell('TOP')

        via_rects = fr.via_center2rects()
        opc_rects = fr.opc_rects
        sraf_rects = fr.sraf_rects
        # rect_names = ['via_rects', 'opc_rects', 'sraf_rects']
        fr_rects = [via_rects, opc_rects, sraf_rects]
        for index, rects in enumerate(fr_rects):
            layer_num = 0
            if index == 0:
                layer_num = VIA_LAYER
            if index == 1:
                layer_num = OPC_LAYER
            if index == 2:
                layer_num = SRAF_LAYER
            rm_rects = remove_margin(fr.center, rects)
            for rect_points in rm_rects:
                rect = gdspy.Rectangle(rect_points[0], rect_points[1], layer=layer_num)
                cell.add(rect)
        outgds_name = 'fr_{}.gds'.format(fr_index)
        outgds_path = os.path.join(out_folder, outgds_name)
        gdsii.write_gds(outgds_path)






def fr2gds(args):
    in_folder = args.in_folder
    out_folder = args.res_folder
    restr = os.path.join(in_folder, '*.gds')
    gds_list = glob.glob(restr)
    for gds in tqdm(gds_list):
        tran_gds(gds, out_folder, args)
