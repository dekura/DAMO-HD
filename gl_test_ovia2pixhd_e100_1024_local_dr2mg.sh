/research/dept7/glchen/miniconda3/envs/guojin/bin/python test_mask_green.py \
--gpu_ids 0 \
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \
--results_dir /research/dept7/glchen/github/pix2pixHD/results \
--dataroot /research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via2/dmo \
--netG local \
--ngf 32 \
--resize_or_crop none \
--name ovia2pixhd_e100_1024_local_dr2mg \
--loadSize 1024 \
--fineSize 1024 \
--which_epoch latest \
--how_many 2000 \
--norm batch \
--label_nc 0 \
--no_instance \
--zip_and_send
