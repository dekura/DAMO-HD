#!/bin/bash
#SBATCH --job-name=v141024
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/dept7/glchen/tmp/log/ovia1pixhd_e100_1024_dr2mg_D2d1.txt
#SBATCH --gres=gpu:1


/research/dept7/glchen/miniconda3/envs/guojin/bin/python train.py \
--gpu_ids 0,1,2,3 \
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \
--dataroot /research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via1/dmo \
--model pix2pixHD \
--netG global \
--batchSize 1 \
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
--name ovia1pixhd_e100_1024_dr2mg_D2d1 \
--max_dataset_size 2000 \
--num_D 2 \
--n_layers_D 1 \
--label_nc 0 \
--no_instance \
--save_latest_freq 2000 \
--save_epoch_freq 10 \
--verbose