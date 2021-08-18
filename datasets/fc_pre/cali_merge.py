'''
@Author: Guojin Chen
@Date: 2020-04-10 11:34:53
LastEditTime: 2021-08-09 14:43:37
@Contact: cgjhaha@qq.com
@Description: merge the merge rounds using calibre
'''
import os
import sys
from tqdm import tqdm
from cali_merge_rule import cali_merge_rule
# import argparse
# import shutil

# parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# parser.add_argument('--input_folder', type=str, default='test_gds', help='where you store the gds')
# parser.add_argument('--name', type=str, default='test', help='the test name')
# args = parser.parse_args()



# def make_dir(dir_path):
#     if not os.path.exists(dir_path):
#         os.makedirs(dir_path)

# def clean_folders(RULE_PATH, LOG_PATH, OUT_PATH):
#     rule_dir = RULE_PATH
#     rule_dir = os.path.join(dir, rule_dir)
#     make_dir(rule_dir)

#     out_dir = OUT_PATH
#     out_dir = os.path.join(dir, out_dir)
#     make_dir(out_dir)

#     log_dir = os.path.join(dir, LOG_PATH)
#     if not os.path.exists(log_dir):
#         # os.mkdir('./log')
#         os.mkdir(log_dir)
#     else:
#         shutil.rmtree(log_dir)
#         os.mkdir(log_dir)

def cali_merge(gds_path, out_gds_path, cell_name, args):
    # calibre_path = 'calibre'
    calibre_path = '/home/hgeng/Calibre/aoj_cal_2018.2_33.24/bin/calibre'
    RULE_PATH = args.rule_folder
    LOG_PATH = args.log_folder
    OUT_PATH = args.out_folder
    rule_dir = RULE_PATH
    # rule_dir = os.path.join(dir, rule_dir)
    sraf_rule = cali_merge_rule(gds_path, out_gds_path)
    rule_name = cell_name + '_cali_merge_rule.cali'
    rule_path = os.path.join(rule_dir, rule_name)
    fs = open(rule_path, 'w+')
    fs.write(sraf_rule)
    fs.close()
    # log_dir = os.path.join(dir, LOG_PATH)
    log_dir = LOG_PATH
    log_name = cell_name + '_cali_merge.log'
    log_path = os.path.join(log_dir, log_name)
    cmd = '{} -drc -hier -64 {} > {}'.format(calibre_path, rule_path, log_path)
    print(cmd)
    os.system(cmd)

def cali(args):
    # calibre_path = '/home/hgeng/Calibre/aoj_cal_2018.2_33.24/bin/calibre'
    # calibre_path = 'calibre'
    # dir = os.path.abspath(os.path.dirname(__file__))
    # clean_folders(RULE_PATH, LOG_PATH, OUT_PATH)
    print('start to using calibre to merge')
    gds_dir = args.dbscan_folder
    # gds_dir = os.path.join(dir, gds_dir)
    # out_dir = os.path.join(dir, OUT_PATH)
    out_dir = args.out_folder
    tbar = tqdm(os.listdir(gds_dir))
    for index, item in enumerate(tbar):
        if item.endswith('.gds'):
            cell_name = item.replace('.gds', '')
            out_name = item.replace('.gds', '_merged.gds')
            gds_path = os.path.join(gds_dir, item)
            out_gds_path = os.path.join(out_dir, out_name)
            cali_merge(gds_path, out_gds_path, cell_name, args)
    print('finish using calibre to merge')

# if __name__ == '__main__':
#     print 'hello gds'
#     main()
