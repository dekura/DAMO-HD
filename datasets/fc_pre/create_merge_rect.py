'''
@Author: Guojin Chen
@Date: 2020-04-09 16:34:47
@LastEditTime: 2020-04-13 17:42:26
@Contact: cgjhaha@qq.com
@Description: add merge rect to the gds
'''
import glob
import gdspy
import numpy as np
import sys
import os
from tqdm import tqdm
from const import LAYERS, PRECISION, MERGE_WH, VIA_WH

VIA_LAYER = LAYERS['design']
OPC_LAYER = LAYERS['mask']
SRAF_LAYER = LAYERS['sraf']
MERGE_LAYER = LAYERS['dbscan']


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

def create_merge_rect(gds_path, outfolder):
    filename = os.path.basename(gds_path)
    GdsIn = gds_path
    gdsii   = gdspy.GdsLibrary()
    lib_out = gdspy.GdsLibrary()

    gdsii.read_gds(GdsIn,units='convert')
    cell    = gdsii.top_level()[0]
    cell_out = lib_out.new_cell('TOP')
    # bbox    = cell.get_bounding_box()
    # print(bbox)
    # bbox:  [[     0.      0.]
    #        [148400. 146000.]]
    # print('width: ', width)
    # print('height: ', height)
    sellayer = [VIA_LAYER, OPC_LAYER, SRAF_LAYER] #Layer Number
    dtype = 0  #Layout Data Type
    token = 1
    for i in tqdm(range(len(sellayer))):
        try:
            polyset = cell.get_polygons(by_spec=True)[(sellayer[i],dtype)]
        except:
            token=0
            print("Layer not found, skipping...")
            break
        for poly in range(0, len(polyset)):
            rect_points = poly_to_rect(polyset[poly])
            rect = gdspy.Rectangle(rect_points[0], rect_points[1], layer=sellayer[i])
            cell_out.add(rect)
            if sellayer[i] == VIA_LAYER:
                merge_points = merge_rect_by_poly(polyset[poly])
                merge_rect = gdspy.Rectangle(merge_points[0], merge_points[1], layer=MERGE_LAYER)
                cell_out.add(merge_rect)
                # merge_round = gdspy.Round(center, MERGE_WH//2, layer=MERGE_LAYER)
                # cell_out.add(merge_round)
    if token == 1:
        filename = filename.replace('.gds', '_dbscan.gds')
        outpath  = os.path.join(outfolder,filename)
        lib_out.write_gds(outpath)


'''
@description: main create
@param {type}:
    args:
        in_folder
        dbscan_folder
@return:
'''
def cmr(args):
    infolder = args.in_folder
    outfolder = args.dbscan_folder
    restr = os.path.join(infolder, '*.gds')
    gds_list = glob.glob(restr)
    print('creating merge rects')
    for gds in tqdm(gds_list):
        create_merge_rect(gds, outfolder)
    print('create merge rects success')


# infolder = sys.argv[1]
# outfolder= sys.argv[2]
# dir = os.path.abspath(os.path.dirname(__file__))
# infolder = os.path.join(dir,'input_gds')
# infolder = '/Users/dekura/Downloads/ispd_in/'
# outfolder = os.path.join(dir,'output_gds')
# outfolder = '/Users/dekura/Downloads/ispd_out/'



