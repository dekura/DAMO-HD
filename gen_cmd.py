'''
@Author: Guojin Chen
@Date: 2020-03-16 11:29:23
@LastEditTime: 2020-04-06 16:33:20
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
parser.add_argument('--train_set_num', type=int, default=2500, help='training set num')
parser.add_argument('--dataroot', type=str, required=True, help='dataroot for train test')
parser.add_argument('--model', type=str, default='pix2pixHD', help='model pix2pixHD | pix2pixw | pix2pixL1')
parser.add_argument('--test_dmo', default=False, action='store_true', help='if gen test script')
parser.add_argument('--epoch', default='latest', type=str, help='test epoch')
parser.add_argument('--test_num', default=5000, type=int, help='test num')
parser.add_argument('--continue_train', default=False, action='store_true', help='whether continue train')
parser.add_argument('--user', default='glchen', type=str, help='python user')
parser.add_argument('--n_layers_D', type=int, default=3, help='only used if which_model_netD==n_layers')
parser.add_argument('--num_D',type=int, default=2, help='how many d to use')
parser.add_argument('--vianum',type=int, default=2, help='the vianum in the training set')
# parser.add_argument('--ndf', type=int, default=64, help='# of discrim filters in first conv layer')
args = parser.parse_args()


def gen_dmo(args):
    gpu_ids = ','.join(str(x) for x in range(args.gpu_num))
    good_prefix = ''
    if 'good' in args.file_name:
        ckp_name = '{}_e{}_{}_good_dr2mg'.format(args.name, 2*args.half_iter, args.load_crop_size)
        good_prefix = 'g'
    else:
        ckp_name = '{}_e{}_{}_dr2mg'.format(args.name, 2*args.half_iter, args.load_crop_size)

    # if args.num_D != 2:
    ckp_name += '_D{}'.format(args.num_D)

    if args.n_layers_D != 3:
        ckp_name += 'd{}'.format(args.n_layers_D)

    if args.load_crop_size == 1024:
        args.resize_or_crop = 'none'
    else:
        args.resize_or_crop = 'scale_width'

    if args.model == 'pix2pixHD':
        model_prefix = ''
    elif args.model == 'pix2pixLR':
        model_prefix = 'lr'
    elif args.model == 'pix2pixL1':
        model_prefix = 'l1'
    else:
        print('no model found')
        return

    if args.user == 'glchen':
        python_inter = '/research/dept7/glchen/miniconda3/envs/guojin/bin/python'
        user_pre = ''
        log_dir = '/research/dept7/glchen/tmp/log'
    elif args.user == 'phchen':
        python_inter = '/research/dept7/glchen/phchen/miniconda3/envs/pytorch/bin/python'
        user_pre = 'ph'
    elif args.user == 'wlchen':
        python_inter = '/research/dept7/wlchen/miniconda3/envs/guojin/bin/python'
        user_pre = 'wl'
        log_dir = '/research/dept7/wlchen/tmp/log'
    elif args.user == 'xiaolin':
        python_inter = '/research/d2/xiaolin/miniconda3/envs/guojin/bin/python'
        user_pre = 'xl'
        log_dir = '/research/d2/xiaolin/tmp/log'
    else:
        print('no this user')
        return

    dmo_code = """#!/bin/bash
#SBATCH --job-name=%s%sv%s%s%d%d
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=%s/%s.txt
#SBATCH --gres=gpu:%d


%s train.py \\
--gpu_ids %s \\
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \\
--dataroot %s \\
--model %s \\
--netG global \\
--batchSize %d \\
--resize_or_crop %s \\
--loadSize %d \\
--fineSize %d \\
--niter %d \\
--niter_decay %d \\
--print_freq %d \\
--input_nc 3 \\
--output_nc 3 \\
--norm instance \\
--data_type 8 \\
--name %s \\
--max_dataset_size %d \\
--num_D %d \\
--n_layers_D %d \\
--label_nc 0 \\
--no_instance \\
--save_latest_freq 2000 \\
--save_epoch_freq 20 \\
--verbose
"""%(user_pre, model_prefix, args.vianum, good_prefix, args.gpu_num, args.load_crop_size, log_dir, ckp_name,
    args.gpu_num, python_inter, gpu_ids, args.dataroot, args.model, args.gpu_num,
    args.resize_or_crop, args.load_crop_size, args.load_crop_size,
    args.half_iter, args.half_iter, args.p_freq, ckp_name, args.train_set_num,
    args.num_D, args.n_layers_D)

    if args.continue_train:
        dmo_code += """--continue_train
"""
    return dmo_code


def gen_test_dmo(args):
    gpu_ids = ','.join(str(x) for x in range(args.gpu_num))
    # ckp_name = '{}_e{}_dr2mg'.format(args.name, 2*args.half_iter)
    # ckp_name = '{}_e{}_{}_dr2mg'.format(args.name, 2*args.half_iter, args.load_crop_size)
    if 'good' in args.file_name:
        ckp_name = '{}_e{}_{}_good_dr2mg'.format(args.name, 2*args.half_iter, args.load_crop_size)
    else:
        ckp_name = '{}_e{}_{}_dr2mg'.format(args.name, 2*args.half_iter, args.load_crop_size)

    # if args.num_D != 2:
    ckp_name += '_D{}'.format(args.num_D)

    if args.n_layers_D != 3:
        ckp_name += 'd{}'.format(args.n_layers_D)
    if args.load_crop_size == 1024:
        args.resize_or_crop = 'none'
    else:
        args.resize_or_crop = 'scale_width'

    if args.model == 'pix2pixHD':
        model_prefix = ''
    elif args.model == 'pix2pixLR':
        model_prefix = 'lr'
    elif args.model == 'pix2pixL1':
        model_prefix = 'l1'
    else:
        print('no model found')
        return

    if args.user == 'glchen':
        python_inter = '/research/dept7/glchen/miniconda3/envs/guojin/bin/python'
    elif args.user == 'phchen':
        python_inter = '/research/dept7/glchen/phchen/miniconda3/envs/pytorch/bin/python'
    elif args.user == 'wlchen':
        python_inter = '/research/dept7/wlchen/miniconda3/envs/guojin/bin/python'
    elif args.user == 'xiaolin':
        python_inter = '/research/d2/xiaolin/miniconda3/envs/guojin/bin/python'
    else:
        print('no this user')
        return

    test_code="""%s test_mask_green.py \\
--gpu_ids %s \\
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \\
--results_dir /research/dept7/glchen/github/pix2pixHD/results \\
--dataroot %s \\
--model %s \\
--netG global \\
--resize_or_crop %s \\
--name %s \\
--loadSize %d \\
--fineSize %d \\
--which_epoch %s \\
--how_many %d \\
--norm instance \\
--label_nc 0 \\
--no_instance \\
--zip_and_send
"""%(python_inter, gpu_ids, args.dataroot, args.model, args.resize_or_crop, ckp_name,
    args.load_crop_size, args.load_crop_size, args.epoch, args.test_num)
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
