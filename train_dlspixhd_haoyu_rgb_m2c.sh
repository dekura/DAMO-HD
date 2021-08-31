#!/bin/bash
#SBATCH --job-name=dmo4
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/dept7/glchen/tmp/log/ovia2pixhd_e100_dr2mg.txt
#SBATCH --gres=gpu:4
# this script is design to train a 2048*2048
# design come from the ganopc dataset
# the mask is generated from the deep levelset generator


/research/d4/gds/gjchen21/miniconda3/envs/pytorch/bin/python train.py \
--gpu_ids 0,1,2,3 \
--checkpoints_dir /research/d4/gds/gjchen21/github/DAMO-HD/checkpoints \
--dataroot /research/d4/gds/gjchen21/datasets/datasets/dlsopc_datasets/via_layouts_0.4_unpaired/dls \
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
--name dls_haoyu_rgb_m2c \
--label_nc 0 \
--no_instance
