#!/bin/bash
#SBATCH --job-name=dls
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/d4/gds/gjchen21/tmp/log/dls_haoyu_rgb_m2c_bdt.txt
#SBATCH --gres=gpu:4
# this script is design to train a 2048*2048
# design come from the ganopc dataset
# the mask is generated from the deep levelset generator
# this use very large dataset


/research/d4/gds/gjchen21/miniconda3/envs/pytorch/bin/python train.py \
--gpu_ids 0,1,2,3 \
--checkpoints_dir /research/d4/gds/gjchen21/github/DAMO-HD/checkpoints \
--dataroot /research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/maskg_contourw_rect_unpaired_rgb_2048 \
--netG global \
--batchSize 4 \
--resize_or_crop resize_and_crop \
--loadSize 1024 \
--fineSize 1024 \
--niter 50 \
--niter_decay 50 \
--print_freq 100 \
--input_nc 3 \
--output_nc 3 \
--norm batch \
--name dls_haoyu_rgb_m2c_bdt \
--label_nc 0 \
--no_instance
