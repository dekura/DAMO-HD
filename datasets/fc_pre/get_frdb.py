'''
@Author: Guojin Chen
@Date: 2020-04-09 13:28:54
@LastEditTime: 2020-05-12 13:52:01
@Contact: cgjhaha@qq.com
@Description: using the k-means++ to cut the window
'''
import os
import shelve
import glob
import gdspy
import numpy as np
from tqdm import tqdm
from shapes import MERGE_RECT, FINAL_RECT
from const import TOTAY_XY, PRECISION, LAYERS
from sklearn.cluster import KMeans

VIA_LAYER = LAYERS['design']
OPC_LAYER = LAYERS['mask']
SRAF_LAYER = LAYERS['sraf']
MERGE_LAYER = LAYERS['dbscan']

def logtxt(info,args):
    txt_name = args.name + '_log.txt'
    txt_path = os.path.join(args.log_folder, txt_name)
    with open(txt_path, mode='a+') as f:
        f.write(info)
'''
get opc polys
'''
def get_opc_sraf_polys(gds_path):
    filename = os.path.basename(gds_path)
    GdsIn = gds_path
    gdsii   = gdspy.GdsLibrary()
    gdsii.read_gds(GdsIn,units='convert')
    cell    = gdsii.top_level()[0]
    sellayer = [OPC_LAYER, SRAF_LAYER]
    dtype = 0  #Layout Data Type
    token = 1
    sellayer = [OPC_LAYER, SRAF_LAYER] #Layer Number
    opc_polys = []
    sraf_polys = []
    for i in range(len(sellayer)):
        try:
            polyset = cell.get_polygons(by_spec=True)[(sellayer[i],dtype)]
        except:
            token=0
            print("Layer not found, skipping...")
            break
        if sellayer[i] == OPC_LAYER:
            opc_polys = polyset
        if sellayer[i] == SRAF_LAYER:
            sraf_polys = polyset
    if token == 1:
        return np.array(opc_polys), np.array(sraf_polys)
'''
good cut:
1. the via belong class i must in the 800 window
2. via <= max_via_in_win
'''
def check_good_cut(mr, nc, y_pred, args):
    for label, cc in enumerate(y_pred.cluster_centers_):
        via_to_label_index = np.where(y_pred.labels_ == label)
        via_centers = mr.vias[via_to_label_index]
        left = cc[0] - ((TOTAY_XY)/2)/PRECISION
        right = left + TOTAY_XY/PRECISION
        down = cc[1] - ((TOTAY_XY)/2)/PRECISION
        up = down + TOTAY_XY/PRECISION
        pos = np.where((via_centers[:, 0] > left) & (via_centers[:, 0] < right) &
        (via_centers[:, 1] > down) & (via_centers[:, 1] < up))
        good_vias = via_centers[pos]
        # print(len(good_vias))
        if (len(good_vias) != len(via_centers)) or (len(good_vias) > args.max_via_in_win):
            # print('nc {} not a good cut'.format(nc))
            return False
    return True

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

def cut_mr(mr, opc_polys, opc_centers, sraf_polys, sraf_centers, args):
    final_rects = []
    for nc in range(1, len(mr.vias)+1):
        y_pred = KMeans(n_clusters=nc).fit(mr.vias)
        if check_good_cut(mr, nc, y_pred, args):
            # print('nc {} is a good cut'.format(nc))
            for label, cc in enumerate(y_pred.cluster_centers_):
                via_to_label_index = np.where(y_pred.labels_ == label)
                via_centers = mr.vias[via_to_label_index]
                fr = FINAL_RECT(cc, via_centers)
                fr.get_opc_rects(opc_polys, opc_centers)
                fr.get_sraf_rects(sraf_polys, sraf_centers)
                final_rects.append(fr)
            break
    return final_rects


def get_frdb(args):
    in_folder = args.stat_folder
    out_folder = args.frdb_folder
    restr = os.path.join(in_folder, '*.gds')
    gds_list = glob.glob(restr)
    for gds in tqdm(gds_list):
        gds_name = os.path.basename(gds)
        mrdb_name = gds_name.replace('.gds', '_mr')
        mrdb_path = os.path.join(in_folder, mrdb_name)
        merge_rects_db = shelve.open(mrdb_path)
        merge_rects = merge_rects_db['merge_rects']

        gds_name = gds_name.replace('_dbscan_merged_stat.gds', '.gds')
        gds_path = os.path.join(args.in_folder, gds_name)
        opc_polys, sraf_polys = get_opc_sraf_polys(gds_path)
        opc_centers = centers_from_polys(opc_polys)
        sraf_centers = centers_from_polys(sraf_polys)
        print('mr has: ', len(merge_rects))
        logtxt('mr has: {}\n'.format(len(merge_rects)), args)
        final_rects = []
        for mr in tqdm(merge_rects):
            frs = cut_mr(mr, opc_polys, opc_centers, sraf_polys, sraf_centers, args)
            final_rects += frs
        print('fr has: ', len(final_rects))
        logtxt('fr has: {}\n'.format(len(final_rects)), args)
        frdb_name = gds_name.replace('.gds', '_fr')
        frdb_path = os.path.join(out_folder, frdb_name)
        db = shelve.open(frdb_path)
        db['final_rects'] = final_rects
        db.close()




