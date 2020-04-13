'''
@Author: Guojin Chen
@Date: 2020-04-12 16:57:37
@LastEditTime: 2020-04-13 14:09:48
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


VIA_LAYER = 0
OPC_LAYER = 1
SRAF_LAYER = 2
BBOX_LAYER = 600
MERGE_LAYER = 400
FR_WIN_LAYER = 800
# PRECISION = 1000
PRECISION = 1000
MERGE_WH = 400
VIA_WH = 70


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

def scale_gds(gds_path, Outfolder):
    filename = os.path.basename(gds_path)
    GdsIn = gds_path
    gdsii   = gdspy.GdsLibrary()
    # gdsii   = gdspy.GdsLibrary()
    lib_out = gdspy.GdsLibrary()
    # lib_out = gdspy.GdsLibrary()

    gdsii.read_gds(GdsIn,units='convert')
    cell    = gdsii.top_level()[0]
    cell_out = lib_out.new_cell('TOP')
    bbox    = cell.get_bounding_box()
    print(bbox)
    # bbox:  [[     0.      0.]
    #        [148400. 146000.]]
    # print('width: ', width)
    # print('height: ', height)
    # bbox_out = gdspy.Rectangle(bbox[0],bbox[1], layer=BBOX_LAYER)
    # cell_out.add(bbox_out)
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
        # if sellayer[i] == VIA_LAYER:
            # centers = np.zeros((len(polyset), 2))
        for poly in range(0, len(polyset)):
            # polyset[poly]
            # [[121925.  56675.]
            # [121975.  56675.]
            # [121975.  56725.]
            # [121925.  56725.]]
            rect_points = poly_to_rect(polyset[poly])
            rect = gdspy.Rectangle(rect_points[0], rect_points[1], layer=sellayer[i])
            cell_out.add(rect)
            # if sellayer[i] == VIA_LAYER:
            #     merge_points = merge_rect_by_poly(polyset[poly])
            #     merge_rect = gdspy.Rectangle(merge_points[0], merge_points[1], layer=MERGE_LAYER)
            #     cell_out.add(merge_rect)
            #     center = center_by_poly(polyset[poly])
            #     centers[poly] = center
                # merge_round = gdspy.Round(center, MERGE_WH//2, layer=MERGE_LAYER)
                # cell_out.add(merge_round)

    db = shelve.open('final_rects')
    final_rects = db['final_rects']
    for fr in tqdm(final_rects):
        rect_points = fr.rect
        rect = gdspy.Rectangle(rect_points[0], rect_points[1], layer=FR_WIN_LAYER)
        cell_out.add(rect)

    if token == 1:
        filename = filename.replace('.gds', '_final_rect.gds')
        outpath  = os.path.join(Outfolder,filename)
        lib_out.write_gds(outpath)
        # txtname = filename.replace('.gds', '_centers.txt')
        # outtxtpath  = os.path.join(Outfolder,txtname)
        # np.savetxt(outtxtpath, centers, fmt='%.5f', delimiter=' ')



# Infolder = sys.argv[1]
# Outfolder= sys.argv[2]
dir = os.path.abspath(os.path.dirname(__file__))
# Infolder = os.path.join(dir,'input_gds')
Infolder = '/Users/dekura/Downloads/ispd_in/'
# Outfolder = os.path.join(dir,'output_gds')
Outfolder = '/Users/dekura/chen/bei/cuDMO/pix2pixHD/datasets/fc_pre/visual/ispd19'


restr = os.path.join(Infolder, '*.gds')
gds_list = glob.glob(restr)

for gds in tqdm(gds_list):
    scale_gds(gds, Outfolder)

print('all rect scaled')