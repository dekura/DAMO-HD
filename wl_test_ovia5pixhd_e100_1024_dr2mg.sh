/research/dept7/wlchen/miniconda3/envs/guojin/bin/python test_mask_green.py \
--gpu_ids 0 \
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \
--results_dir /research/dept7/glchen/github/pix2pixHD/results \
--dataroot /research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via5/dmo \
--model pix2pixHD \
--netG global \
--resize_or_crop none \
--name ovia5pixhd_e100_1024_dr2mg \
--loadSize 1024 \
--fineSize 1024 \
--which_epoch 100 \
--how_many 500 \
--norm instance \
--label_nc 0 \
--no_instance \
--zip_and_send
