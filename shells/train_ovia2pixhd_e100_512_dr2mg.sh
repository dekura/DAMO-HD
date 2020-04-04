#!/bin/bash
#SBATCH --job-name=hd1512
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/dept7/glchen/tmp/log/ovia2pixhd_e100_512_dr2mg.txt
#SBATCH --gres=gpu:1


/research/dept7/glchen/miniconda3/envs/guojin/bin/python train.py \
--gpu_ids 0 \
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \
--dataroot /research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via2/dmo \
--netG global \
--batchSize 1 \
--resize_or_crop scale_width \
--loadSize 512 \
--fineSize 512 \
--niter 50 \
--niter_decay 50 \
--print_freq 500 \
--input_nc 3 \
--output_nc 3 \
--norm instance \
--data_type 8 \
--name ovia2pixhd_e100_512_dr2mg \
--label_nc 0 \
--no_instance \
--save_latest_freq 2000 \
--save_epoch_freq 20
