#!/bin/bash
#SBATCH --job-name=wlhd41024
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/dept7/glchen/tmp/log/1ovia4pixhd_e100_1024_dr2mg_nd1.txt
#SBATCH --gres=gpu:4


/research/dept7/wlchen/miniconda3/envs/guojin/bin/python train.py \
--gpu_ids 0 \
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \
--dataroot /research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via4/dmo \
--model pix2pixHD \
--netG global \
--n_layers_D 1 \
--ndf 8 \
--batchSize 1 \
--resize_or_crop none \
--loadSize 1024 \
--fineSize 1024 \
--niter 50 \
--niter_decay 50 \
--print_freq 500 \
--input_nc 3 \
--output_nc 3 \
--norm instance \
--data_type 8 \
--name 1ovia4pixhd_e100_1024_dr2mg_nd1 \
--label_nc 0 \
--no_instance \
--save_latest_freq 2000 \
--save_epoch_freq 20
