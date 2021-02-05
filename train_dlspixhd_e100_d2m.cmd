#!/bin/bash
#SBATCH --job-name=dls
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/d2/xfyao/guojin/tmp/log/dlspixhd_e100_d2m.txt
#SBATCH --gres=gpu:4

/research/d2/xfyao/tools/anaconda3/envs/maskrcnn/bin/python train.py \
--gpu_ids 0,1,2,3 \
--checkpoints_dir /research/d2/xfyao/guojin/pix2pixHD/checkpoints \
--dataroot /research/d2/xfyao/guojin/data/datasets/develset/ \
--netG global \
--batchSize 4 \
--resize_or_crop resize_and_crop \
--loadSize 1024 \
--fineSize 1024 \
--niter 50 \
--niter_decay 50 \
--print_freq 500 \
--input_nc 3 \
--output_nc 3 \
--norm batch \
--name dls_e100_d2m \
--label_nc 0 \
--no_instance \
--save_epoch_freq 10
