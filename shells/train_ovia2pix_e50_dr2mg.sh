#!/bin/bash
#SBATCH --job-name=dmo1
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/dept7/glchen/tmp/log/ovia2pixw_e50_dr2mg.txt
#SBATCH --gres=gpu:1

/research/dept7/glchen/miniconda3/envs/guojin/bin/python train.py \
--gpu_ids 0 \
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \
--dataroot /research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via2/dmo \
--netG global \
--batchSize 1 \
--resize_or_crop none \
--loadSize 1024 \
--fineSize 1024 \
--niter 25 \
--niter_decay 25 \
--print_freq 100 \
--input_nc 3 \
--output_nc 3 \
--norm batch \
--name ovia2pixhd_e50_dr2mg \
--label_nc 0 \
--no_instance \
--tf_log
