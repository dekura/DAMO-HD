'''
@Author: Guojin Chen
@Date: 2020-03-14 20:06:06
@LastEditTime: 2020-05-05 10:21:28
@Contact: cgjhaha@qq.com
@Description: get train test dataset by via
'''
import re
import os
import sys
import glob
import random
from tqdm import tqdm
from get_polys import get_poly_vianum
from utils.database import EPE_DB


def get_names_good(args):
    db_path = args.sqldb_path
    epedb = EPE_DB(db_path)
    epedb.parse_mepe()
    epebar = args.epebar
    # names : set()
    names = epedb.get_names_mepeless(epebar)
    return names
'''
@description: separate the given gds from different via num
@param {type} args {
    gds_path{str} : input gds_folder path
}
@return: list_by_via{
    '1': [] list of via_num = 1,
    ...
}
'''
def get_detail_list(args):
    restr = os.path.join(args.gds_path, args.gds_post)
    gds_list = glob.glob(restr)
    gds_list.sort()
    list_by_via = {}
    if args.gen_good:
        better_names = get_names_good(args)
    for item in tqdm(gds_list):
        via_num = get_poly_vianum(item, args)
        if via_num:
            via_num = str(via_num)
            if not via_num in list_by_via:
                list_by_via[via_num] = []
            if args.gen_good:
                gdsname = os.path.basename(item)
                cell_id = re.findall(r"\d+", gdsname)[0]
                cell_name = 'via{}'.format(cell_id)
                if cell_name in better_names:
                    list_by_via[via_num].append(item)
            else:
                list_by_via[via_num].append(item)
    return list_by_via


def gen_dataset(args):
    test_data = []
    train_data = []
    list_by_via = get_detail_list(args)
    for via_num, via_num_list in list_by_via.items():
        print('via num {}: has {} data'.format(via_num, len(via_num_list)))
        max_pervia = min(len(via_num_list), args.max_pervia)
        via_num_list = via_num_list[:max_pervia]
        print('now set via num {}: to be {} data'.format(via_num, max_pervia))
        test_num = len(via_num_list)//args.test_ratio
        via_test = via_num_list[:test_num]
        via_train = via_num_list[test_num:]
        test_data = test_data + via_test
        train_data = train_data + via_train
    return test_data, train_data


'''
@description: separate the given gds from different via num
@param {type} args {
    gds_path{str} : input gds_folder path
}
@return: set_byvia{
    '1': ([],[]) list of via_num = 1, (test_set, train_set)
    ...
}
'''

def gen_set_byvia(args):
    list_by_via = get_detail_list(args)
    set_byvia = {}
    for via_num, via_num_list in list_by_via.items():
        if not via_num in args.gen_via_lists:
            continue
        print('via num {}: has {} data'.format(via_num, len(via_num_list)))
        max_pervia = min(len(via_num_list), args.max_pervia)
        # via_num_list = via_num_list[:max_pervia]
        via_num_list = random.sample(via_num_list, max_pervia)
        print('now set via num {}: to be {} data'.format(via_num, max_pervia))
        if args.gen_seen_set:
            # via_test = via_num_list[:test_num]
            test_num = len(via_num_list)//args.test_ratio
            via_train = via_num_list
            via_test = random.sample(via_train, test_num)
            set_byvia[via_num] = (via_test, via_train)
        else:
            test_num = len(via_num_list)//args.test_ratio
            via_test = via_num_list[:test_num]
            via_train = via_num_list[test_num:]
            set_byvia[via_num] = (via_test, via_train)
    return set_byvia




def gen_set_byvia_from_train(args):
    print('get via list from training set')
    vianum = 4
    set_byvia = {}
    train_A = '/research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via{}_unseen/dmo/train_A'.format(vianum)
    restr = os.path.join(train_A, '*.png')
    png_list = glob.glob(restr)
    png_list.sort()
    id_list = []
    for png in png_list:
        pngname = os.path.basename(png)
        cell_id = re.findall(r"\d+", pngname)[0]
        id_list.append(cell_id)

    test_id_list = random.sample(id_list, 400)
    test_gds_list = []
    gds_folder = '/research/dept7/glchen/datasets/gds/ovia{}/gds'.format(vianum)
    for tid in test_id_list:
        gds_name = 'via{}_mbsraf.gds_lccout_CALI.gds'.format(tid)
        gds_path = os.path.join(gds_folder, gds_name)
        test_gds_list.append(gds_path)

    set_byvia[str(vianum)] = (test_gds_list, [])
    return set_byvia