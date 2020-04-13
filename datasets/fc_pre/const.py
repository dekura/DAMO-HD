'''
@Author: Guojin Chen
@Date: 2020-03-11 15:03:02
@LastEditTime: 2020-04-12 18:14:10
@Contact: cgjhaha@qq.com
@Description: some consts
'''

LAYERS = {
    'design': 0,
    'mask': 1,
    'sraf': 2,
    'wafer': 200,
    'dbscan': 400
}

DIRS = ['train_A', 'train_B', 'test_A', 'test_B' , 'testbg']


# PRECISION = 1000
PRECISION = 1000
# const for the dbscan w and h
MERGE_WH = 400
# the via w and h
VIA_WH = 70
# the useful area in a 1024 window
TOTAY_XY = 700
# the opc window size
VIA_WIN_WH = 1024
