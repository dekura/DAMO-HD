#!/bin/bash
#SBATCH --job-name=hd4512
#SBATCH --mail-user=cgjhaha@qq.com
#SBATCH --mail-type=ALL
#SBATCH --output=/research/dept7/glchen/tmp/log/ovia4pixhd_e100_512_local_dr2mg.txt
#SBATCH --gres=gpu:4


/research/dept7/glchen/miniconda3/envs/guojin/bin/python train.py \
--gpu_ids 0,1,2,3 \
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \
--dataroot /research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via4/dmo \
--model pix2pixHD \
--netG local \
--ngf 32 \
--num_D 3 \
--batchSize 4 \
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
--name ovia4pixhd_e100_512_local_dr2mg \
--max_dataset_size 2500 \
--label_nc 0 \
--no_instance \
--save_latest_freq 2000 \
--save_epoch_freq 20 \
--tf_log \
--load_pretrain checkpoints/_e_512_dr2mg/ \
--niter_fix_global 10
