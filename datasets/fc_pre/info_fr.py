'''
@Author: Guojin Chen
@Date: 2020-04-16 16:52:44
LastEditTime: 2021-08-14 00:55:25
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

def info(gds, args):
    filename = os.path.basename(gds)
    frdb_name = filename.replace('.gds','_fr')
    frdb_path = os.path.join(args.frdb_folder, frdb_name)
    db = shelve.open(frdb_path)
    final_rects = db['final_rects']
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