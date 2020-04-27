#!/bin/bash
#SBATCH --job-name=xlt2
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/d2/xiaolin/tmp/log/test_ovia2pixhd_e100_1024_good_dr2mg_D2d1.txt
#SBATCH --gres=gpu:1

/research/d2/xiaolin/miniconda3/envs/guojin/bin/python test_mask_green.py \
--gpu_ids 0 \
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \
--results_dir /research/dept7/glchen/github/pix2pixHD/results \
--dataroot /research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via2_good/dmo \
--model pix2pixHD \
--netG global \
--resize_or_crop none \
--name ovia2pixhd_e100_1024_good_dr2mg_D2d1 \
--loadSize 1024 \
--fineSize 1024 \
--which_epoch latest \
--how_many 1000 \
--norm instance \
--label_nc 0 \
--no_instance \
--zip_and_send
