#!/bin/bash
#SBATCH --job-name=dmo4
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/dept7/glchen/tmp/log/ovia2pixhd_e100_dr2mg.txt
#SBATCH --gres=gpu:4
# this script is design to train a 2048*2048
# design come from the ganopc dataset
# the mask is generated from the deep levelset generator


/research/dept7/glchen/miniconda3/envs/guojin/bin/python train.py \
--gpu_ids 0,1,2,3 \
--checkpoints_dir /research/d2/xfyao/guojin/pix2pixHD/checkpoints \
--dataroot /research/d2/xfyao/guojin/data/datasets/develset/pngs \
--netG global \
--batchSize 4 \
--resize_or_crop resize_and_crop \
--loadSize 1024 \
--fineSize 1024 \
--niter 50 \
--niter_decay 50 \
--print_freq 500 \
--input_nc 1 \
--output_nc 1 \
--norm batch \
--name dls_e100_d2m \
--label_nc 0 \
--no_instance \
--tf_log
