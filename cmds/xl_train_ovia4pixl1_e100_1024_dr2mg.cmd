#!/bin/bash
#SBATCH --job-name=xll1v4g
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/d2/xiaolin/tmp/log/ovia4pixl1_e100_1024_dr2mg.txt
#SBATCH --gres=gpu:4


/research/d2/xiaolin/miniconda3/envs/guojin/bin/python train.py \
--gpu_ids 0,1,2,3 \
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \
--dataroot /research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via4/dmo \
--model pix2pixL1 \
--netG global \
--batchSize 4 \
--resize_or_crop none \
--loadSize 1024 \
--fineSize 1024 \
--niter 50 \
--niter_decay 50 \
--print_freq 100 \
--input_nc 3 \
--output_nc 3 \
--norm instance \
--data_type 8 \
--name ovia4pixl1_e100_1024_dr2mg \
--max_dataset_size 2500 \
--label_nc 0 \
--no_instance \
--save_latest_freq 2000 \
--save_epoch_freq 20 \
--verbose \
--tf_log
