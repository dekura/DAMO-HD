'''
@Author: Guojin Chen
@Date: 2020-03-16 11:29:23
@LastEditTime: 2020-03-22 23:07:01
@Contact: cgjhaha@qq.com
@Description: make command for train or testing
'''
import os
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--name', type=str, default='layout_0.4', help='experiment name')
parser.add_argument('--file_name', type=str, default='dmo4.cmd', help='the cmd file name')
parser.add_argument('--gpu_num', type=int, default=4, help='how many gpu you need.')
parser.add_argument('--half_iter', type=int, default=35, help='half of total iter')
parser.add_argument('--p_freq', type=int, default=500, help='print frequence')
parser.add_argument('--load_crop_size', type=int, default=1024, help='load and crop size')
parser.add_argument('--dataroot', type=str, required=True, help='dataroot for train test')
parser.add_argument('--model', type=str, default='pix2pixHD', help='model pix2pixHD | pix2pixw')
parser.add_argument('--test_dmo', default=False, action='store_true', help='if gen test script')
parser.add_argument('--epoch', default='latest', type=str, help='test epoch')
parser.add_argument('--test_num', default=1000, type=int, help='test num')
parser.add_argument('--continue_train', default=False, action='store_true', help='whether continue train')
parser.add_argument('--pretrain_512', required=True, help='the pretrain 512 g')
args = parser.parse_args()


def gen_dmo(args):
    gpu_ids = ','.join(str(x) for x in range(args.gpu_num))
    ckp_name = '{}_e{}_{}_local_dr2mg'.format(args.name, 2*args.half_iter, args.load_crop_size)
    dmo_code = """#!/bin/bash
#SBATCH --job-name=l%d%d
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/dept7/glchen/tmp/log/%s.txt
#SBATCH --gres=gpu:%d


/research/dept7/glchen/miniconda3/envs/guojin/bin/python train.py \\
--gpu_ids %s \\
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \\
--dataroot %s \\
--netG local \\
--ngf 32 \\
--num_D 3 \\
--batchSize %d \\
--resize_or_crop none \\
--loadSize %d \\
--fineSize %d \\
--niter %d \\
--niter_decay %d \\
--print_freq %d \\
--input_nc 3 \\
--output_nc 3 \\
--norm batch \\
--data_type 8 \\
--name %s \\
--label_nc 0 \\
--no_instance \\
--save_latest_freq 2000 \\
--save_epoch_freq 20 \\
--load_pretrain %s \\
--niter_fix_global 10
"""%(args.gpu_num, args.load_crop_size, ckp_name, args.gpu_num, gpu_ids, args.dataroot,
    args.gpu_num, args.load_crop_size, args.load_crop_size,
    args.half_iter, args.half_iter, args.p_freq, ckp_name, args.pretrain_512)

    if args.continue_train:
        dmo_code += """--continue_train
"""
    return dmo_code


def gen_test_dmo(args):
    gpu_ids = ','.join(str(x) for x in range(args.gpu_num))
    # ckp_name = '{}_e{}_dr2mg'.format(args.name, 2*args.half_iter)
    ckp_name = '{}_e{}_{}_dr2mg'.format(args.name, 2*args.half_iter, args.load_crop_size)
    test_code="""/research/dept7/glchen/miniconda3/envs/guojin/bin/python test_mask_green.py \\
--gpu_ids %s \\
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \\
--results_dir /research/dept7/glchen/github/pix2pixHD/results \\
--dataroot %s \\
--netG global \\
--resize_or_crop none \\
--name %s \\
--loadSize %d \\
--fineSize %d \\
--which_epoch %s \\
--how_many %d \\
--norm batch \\
--label_nc 0 \\
--no_instance
"""%(gpu_ids, args.dataroot, ckp_name, args.load_crop_size,
    args.load_crop_size, args.epoch, args.test_num)
    return test_code

def main(args):
    if args.test_dmo:
        code = gen_test_dmo(args)
    else:
        code = gen_dmo(args)
    print(code)
    with open(args.file_name, 'w+') as f:
        f.write(code)


if __name__ == '__main__':
    main(args)
