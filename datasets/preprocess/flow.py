'''
@Author: Guojin Chen
@Date: 2020-03-09 20:19:13
@LastEditTime: 2020-04-15 09:30:09
@Contact: cgjhaha@qq.com
@Description: the gds to png flow

gds to png:
1. gds to (design + sraf) : (mask + design + sraf) : (wafer), all is rgb three channels
2. copy images to dataset for training
3. DMO: (design + sraf)+(mask + design + sraf);
4. DLS: (mask + design + sraf) : (wafer)

/data/dmo/train
/data/dmo/test
'''


import os
import glob
import time
import tarfile
import argparse
import numpy as np
from tqdm import tqdm
from PIL import Image
from consts import LAYERS, DIRS
from get_polys import get_polys
from gen_im import gen_d_m_s, gen_d_s, gen_w
from gen_dataset import gen_dataset, gen_set_byvia, gen_set_byvia_from_train

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--name', type=str, default='layout_0.4', help='experiment name')
parser.add_argument('--load_size', type=int, default=2048, help='image load size')
parser.add_argument('--crop_size', type=int, default=1024, help='then crop into this size for training')
parser.add_argument('--test_ratio', type=int, default=4, help='testset ratio. eg: 4: 0.25, 5:0.2')
parser.add_argument('--max_pervia', type=int, default=2000, help='max test+train num one via')
parser.add_argument('--for_dmo', default=False, action='store_true', help='for dmo')
parser.add_argument('--for_dls', default=False, action='store_true', help='for dls')
parser.add_argument('--set_byvia', default=False, action='store_true', help='whether gen set by via')
parser.add_argument('--gen_via_lists', type=str, default='1,2', help='which vianum subdataset to gen, 1,2,3,4')
parser.add_argument('--gen_seen_set', default=False, action='store_true', help='if true, get test set from train set')
parser.add_argument('--gds_path', type=str, required=True, help='the input gds path')
parser.add_argument('--out_folder', type=str, required=True, help='output data folder')
parser.add_argument('--gen_good', default=False, action='store_true', help='if gen_good, will get info from sqldb to gen better epe dataset')
parser.add_argument('--sqldb_path', default='./', type=str, help='the sqldb path for one via gen')
parser.add_argument('--epebar', default=0.6 , type=float, help='epebar for good dataset')
parser.add_argument('--gen_only_test', default=False, action='store_true', help='whether gen only test set')
# out_folder/dmo/trainA
# out_folder/dls/trainA
args = parser.parse_args()

if args.gen_only_test:
    DIRS = ['test_A', 'test_B' , 'testbg']
    args.test_ratio = 1
    args.gen_seen_set = False
    args.gen_good = False


def save_im(imA, imB, dataset_type, sub_type, item_name, args):
    # save_path = os.path.join(args._root_folder, sub_type, dataset_type)
    # path_AB = os.path.join(save_path, item_name+'.png')
    if dataset_type == 'testbg':
        # imAB = np.concatenate([np.array(imA), np.array(imB)], 1)
        # imAB = imB
        pathB = os.path.join(args._root_folder, sub_type, dataset_type)
        pathB = os.path.join(pathB, item_name+'.png')
        imB.save(pathB)
    else:
        pathA = os.path.join(args._root_folder, sub_type, dataset_type+'_A')
        pathB = os.path.join(args._root_folder, sub_type, dataset_type+'_B')
        pathA = os.path.join(pathA, item_name+'.png')
        pathB = os.path.join(pathB, item_name+'.png')
        # first crop the image
        if os.path.isfile(pathA) or os.path.isfile(pathB):
            print('file already exist ... pass')
            return
        left = (args.load_size - args.crop_size)//2
        top = left
        right = left + args.crop_size
        down = top + args.crop_size
        imA_crop = imA.crop((left, top, right, down))
        imB_crop = imB.crop((left, top, right, down))
        imA_crop.save(pathA)
        imB_crop.save(pathB)
        # imAB = Image.fromarray(imAB.astype('uint8')).convert('RGB')
        # imAB = np.concatenate([np.array(imA_crop), np.array(imB_crop)], 1)



# def check_img_exist(args):
#     save_path = os.path.join(args._root_folder, sub_type, dataset_type)
#     path_AB = os.path.join(save_path, item_name+'.png')


#一次性打包整个根目录。空子目录会被打包。
#如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
def make_targz(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def tar_testbg(sub_type, args):
    dataset_type = 'testbg'
    testbg_path = os.path.join(args._root_folder, sub_type, dataset_type)
    testbg_tar_path = os.path.join(args._root_folder, sub_type, 'testbg.tar.gz')
    if not os.path.exists(testbg_path):
        print('testbg path {} not found'.format(testbg_path))
        raise NotADirectoryError
    make_targz(testbg_tar_path, testbg_path)

def gen_data(dataset, dataset_type, args):
    print('generating {} set'.format(dataset_type))
    print('dataset paths is {}'.format(os.path.join(args._root_folder, dataset_type)))
    for item in tqdm(dataset):
        item_name = os.path.splitext(os.path.basename(item))[0]
        # load_size polys
        polys = get_polys(item, args)
        if not polys:
            print('polys not found')
            continue
        # load_size dms
        dms = gen_d_m_s(polys, args)
        if args.for_dmo:
            ds = gen_d_s(polys, args)
            save_im(ds, dms, dataset_type, 'dmo', item_name, args)
        if args.for_dls:
            wafer = gen_w(polys, args)
            save_im(dms, wafer, dataset_type, 'dls', item_name, args)

    if dataset_type == 'testbg':
        if args.for_dmo:
            tar_testbg('dmo', args)
        if args.for_dls:
            tar_testbg('dls', args)





def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def prepare_subdirs(root_folder, sub_type):
    sub_path = os.path.join(root_folder, sub_type)
    makedir(sub_path)
    for subsubdir in DIRS:
        subsubpath = os.path.join(sub_path, subsubdir)
        makedir(subsubpath)

'''
out_folder
    dmo
        train
        test
        testbg
'''
def prepare_dirs(args):
    makedir(args._root_folder)
    if args.for_dmo:
        prepare_subdirs(args._root_folder, 'dmo')
    if args.for_dls:
        prepare_subdirs(args._root_folder, 'dls')


def main():
    print(args)
    t = time.time()
    if not os.path.exists(args.gds_path):
        raise FileNotFoundError
    makedir(args.out_folder)
    if args.set_byvia:
        set_byvia = gen_set_byvia(args)
        # set_byvia = gen_set_byvia_from_train(args)
        for via_num, sets in set_byvia.items():
            if args.gen_good:
                args._root_folder = os.path.join(args.out_folder, 'via{}_good'.format(via_num))
            else:
                args._root_folder = os.path.join(args.out_folder, 'via{}'.format(via_num))
            prepare_dirs(args)
            test_set, train_set = sets
            gen_data(test_set, 'test', args)
            gen_data(test_set, 'testbg', args)
            if not args.gen_only_test:
                gen_data(train_set, 'train', args)
    else:
        args._root_folder = args.out_folder
        prepare_dirs(args)
        test_set, train_set = gen_dataset(args)
        gen_data(test_set, 'test', args)
        gen_data(test_set, 'testbg', args)
        if not args.gen_only_test:
            gen_data(train_set, 'train', args)

    elapsed = time.time() - t
    print('total running time: {}'.format(elapsed))

if __name__ == '__main__':
    main()
