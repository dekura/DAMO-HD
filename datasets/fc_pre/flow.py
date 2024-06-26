'''
@Author: Guojin Chen
@Date: 2020-04-09 16:00:12
LastEditTime: 2021-08-19 07:58:51
@Contact: cgjhaha@qq.com
@Description: total flow
'''
import os
import glob
import time
import argparse
import numpy as np
from create_merge_rect import cmr
from cali_merge import cali
from get_mrdb import get_mrdb
from get_frdb import get_frdb
from visual_fr import visual_fr
from fr2gds import fr2gds
from info_fr import info_fr, logtxt
from merge_dmo import merge_dmo

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--name', type=str, default='ispd19', help='experiment name')
parser.add_argument('--in_folder', type=str, required=True, help='the input gds path')
parser.add_argument('--dbscan_folder', type=str, default='./dbscan', help='the dbscan save folder')
parser.add_argument('--out_folder', type=str, default='./out_gds', help='output data folder')
parser.add_argument('--rule_folder', type=str, default='./rule', help='folder to save rules')
parser.add_argument('--log_folder', type=str, default='./log', help='folder to save logs')
parser.add_argument('--stat_folder', type=str, default='./stat', help='folder to save mr stat')
parser.add_argument('--frdb_folder', type=str, default='./frdb', help='folder to save fr db')
parser.add_argument('--vis_folder', type=str, default='./visual', help='folder to save fr visual')
parser.add_argument('--res_folder', type=str, default='./results', help='folder to save fr results')
parser.add_argument('--max_via_in_win', type=int, default=5, help='max via num in a split window')
parser.add_argument('--dmo_res_folder', type=str, default='', help='the dmo results for merge gds')
parser.add_argument('--dmo_merged_folder', type=str, default='./dmo_merged', help='the merged gds store folder')
args = parser.parse_args()


def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def predir(args):
    args.dbscan_folder = os.path.join(args.dbscan_folder, args.name)
    makedir(args.dbscan_folder)
    args.out_folder = os.path.join(args.out_folder, args.name)
    makedir(args.out_folder)
    args.rule_folder = os.path.join(args.rule_folder, args.name)
    makedir(args.rule_folder)
    args.log_folder = os.path.join(args.log_folder, args.name)
    makedir(args.log_folder)
    args.stat_folder = os.path.join(args.stat_folder, args.name)
    makedir(args.stat_folder)
    args.frdb_folder = os.path.join(args.frdb_folder, args.name)
    makedir(args.frdb_folder)
    args.vis_folder = os.path.join(args.vis_folder, args.name)
    makedir(args.vis_folder)
    args.res_folder = os.path.join(args.res_folder, args.name)
    makedir(args.res_folder)
    args.dmo_merged_folder = os.path.join(args.dmo_merged_folder, args.name)
    makedir(args.dmo_merged_folder)



t = time.time()
logtxt('testing time : {} \n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), args)


predir(args)
'''
get all via and set a merge rect outside 510
save them to dbscan folder
'''
# cmr(args)

'''
merge them using calibre
'''

# cali(args)

'''
store all via center
store all merge_rect center and areas
for the mergt_rect that are longer than 1024
other algorithms.
'''
# get_mrdb(args)

'''
cut the mr(merge_rects) to fr(final_rects)
'''
# get_frdb(args)

'''
Visual the fr
'''
# visual_fr(args)

'''
analysis the vianum distribution
how many 1 2 3 4 5 6 in this way
'''
info_fr(args)

'''
create fr to a small window gds
'''

# fr2gds(args)

'''
merge all the final rects
'''
# merge_dmo(args)

elapsed = time.time() - t
print('total running time: {}'.format(elapsed))
logtxt('total running time: {}\n\n'.format(elapsed), args)