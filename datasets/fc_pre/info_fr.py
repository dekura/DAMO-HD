'''
@Author: Guojin Chen
@Date: 2020-04-16 16:52:44
LastEditTime: 2021-08-19 08:18:28
@Contact: cgjhaha@qq.com
@Description: get final rects infomations
'''
import os
import sys
import glob
import shelve
import numpy as np
from tqdm import tqdm

def logtxt(info,args):
    txt_name = args.name + '_log.txt'
    txt_path = os.path.join(args.log_folder, txt_name)
    with open(txt_path, mode='a+') as f:
        f.write(info)


def get_centers(final_rects):
    fr_centers = []
    for fr in tqdm(final_rects):
        print(fr.center)
        fr_centers.append(fr.center)
    fr_centers = np.array(fr_centers)
    np.savetxt('./centers.txt', fr_centers)


def info(gds, args):
    filename = os.path.basename(gds)
    frdb_name = filename.replace('.gds','_fr')
    frdb_path = os.path.join(args.frdb_folder, frdb_name)
    db = shelve.open(frdb_path)
    # print(db)
    final_rects = db['final_rects']
    # get_centers(final_rects)
    via_dt = {}
    for i in range(1,args.max_via_in_win+1):
        via_dt[str(i)] = 0
    for fr in tqdm(final_rects):
        via_num = len(fr.vias)
        via_dt[str(via_num)] += 1
    print(via_dt)
    logtxt(str(via_dt)+'\n', args)


def info_fr(args):
    in_folder = args.in_folder
    restr = os.path.join(in_folder, '*.gds')
    gds_list = glob.glob(restr)
    for gds in tqdm(gds_list):
        info(gds, args)