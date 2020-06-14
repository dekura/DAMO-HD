'''
@Author: Guojin Chen
@Date: 2020-05-12 09:17:56
@LastEditTime: 2020-05-12 23:32:59
@Contact: cgjhaha@qq.com
@Description: merge the dmo results
'''
import os
import re
import glob
import gdspy
import shelve
import numpy as np
from tqdm import tqdm
from const import LAYERS, GDS_WIN_WH, PRECISION, BBOX_WH

VIA_LAYER = LAYERS['design']
OPC_LAYER = LAYERS['mask']
SRAF_LAYER = LAYERS['sraf']
MERGE_LAYER = LAYERS['dbscan']
BBOX_LAYER = LAYERS['bbox']

# def remove_margin(fr_center, rects):
#     left_margin = fr_center[0] - (GDS_WIN_WH/2)/PRECISION
#     down_margin = fr_center[1] - (GDS_WIN_WH/2)/PRECISION
#     for rect in rects:
#         rect[0][0] -= left_margin
#         rect[0][1] -= down_margin
#         rect[1][0] -= left_margin
#         rect[1][1] -= down_margin
#     return rects

# def center2bbox(fr_center):
#     center = fr_center
#     left = center[0] - (BBOX_WH/2)/PRECISION
#     right = left + BBOX_WH/PRECISION
#     down = center[1] - (BBOX_WH/2)/PRECISION
#     up = down + BBOX_WH/PRECISION
#     point1 = np.array([left, down])
#     point2 = np.array([right, up])
#     rect = (point1, point2)
#     return [rect]

def poly_to_rect(poly):
    xl = poly[0][0]  # 25
    xr = poly[1][0]  # 75
    yd = poly[0][1]  # 25
    yu = poly[2][1]  # 75
    point1 = np.array([xl, yd])
    point2 = np.array([xr, yu])
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

def centers_from_polys(polys):
    centers = np.zeros((len(polys), 2))
    for index, poly in enumerate(polys):
        centers[index] = center_by_poly(poly)
    return centers

'''
@description: cell to get relative opc rects
@param {type} cell gdspy
@return: [opc rects]
'''
def cell2relrects(cell):
    dtype = 0
    viapolys = cell.get_polygons(by_spec=True)[(VIA_LAYER,dtype)]
    via_centers = centers_from_polys(viapolys)
    cx = np.mean(via_centers[:,0])
    cx = np.mean(via_centers[:,1])
    opcpolys = cell.get_polygons(by_spec=True)[(OPC_LAYER,dtype)]
    for opcpoly in opcpolys:
        for i in range(len(opcpoly)):
            opcpoly[i][0] -= cx
            opcpoly[i][1] -= cy
    return opcpolys

def get_mask_layer(cell, final_rects, gds, args):
    dtype = 0
    filename = os.path.basename(gds)
    fr_id = re.findall(r"\d+", filename)[0]
    fr_id = int(fr_id)
    gdspy.current_library = gdspy.GdsLibrary()
    gdsfr = gdspy.GdsLibrary()
    gdsfr.read_gds(gds)
    fr_cell = gdsfr.top_level()[0]
    fr_opc_polys = fr_cell.get_polygons(by_spec=True)[(OPC_LAYER,dtype)]
    big_cx = final_rects[fr_id].center[0]
    big_cy = final_rects[fr_id].center[1]
    for poly in fr_opc_polys:
        for i in range(len(poly)):
            poly[i][0] += big_cx
            poly[i][1] += big_cy
        rect_points = poly_to_rect(poly)
        rect = gdspy.Rectangle(rect_points[0], rect_points[1], layer=OPC_LAYER)
        cell.add(rect)


def get_design_sraf_layer(cell, init_gds, args):
    dtype = 0
    gdspy.current_library = gdspy.GdsLibrary()
    init_lib = gdspy.GdsLibrary()
    init_lib.read_gds(init_gds)
    init_cell = init_lib.top_level()[0]
    all_layers = [VIA_LAYER, SRAF_LAYER]
    for layer in all_layers:
        polys = init_cell.get_polygons(by_spec=True)[(layer,dtype)]
        outpolysets = gdspy.PolygonSet(polys, layer=layer, datatype=dtype)
        cell.add(outpolysets)







def merge_dmo(args):
    in_folder = args.dmo_res_folder
    out_folder = args.dmo_merged_folder
    frdb_path = '/research/dept7/glchen/github/pix2pixHD/datasets/fc_pre/frdb/ispd19fc5/ispd19_test_fr'
    init_gds = '/research/dept7/glchen/github/pix2pixHD/datasets/fc_pre/test_gds/ispd19test/ispd19_test.gds'
    db = shelve.open(frdb_path)
    final_rects = db['final_rects']
    restr = os.path.join(in_folder, '*/gds/*_GAN.gds')
    gds_list = glob.glob(restr)
    gdspy.current_library = gdspy.GdsLibrary()
    gdsii = gdspy.GdsLibrary()
    cell = gdsii.new_cell('TOP')
    for gds in tqdm(gds_list):
        get_mask_layer(cell, final_rects, gds, args)
    get_design_sraf_layer(cell, init_gds, args)
    outgds_name = 'ispd19fc5_dmo.gds'
    outgds_path = os.path.join(out_folder, outgds_name)
    gdsii.write_gds(outgds_path)
