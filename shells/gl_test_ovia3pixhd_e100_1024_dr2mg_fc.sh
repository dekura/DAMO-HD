# 5 fc_results 6 fchdsep 13 10000
/research/dept7/glchen/miniconda3/envs/guojin/bin/python test_mask_green.py \
--gpu_ids 0 \
--checkpoints_dir /research/dept7/glchen/github/pix2pixHD/checkpoints \
--results_dir /research/dept7/glchen/github/pix2pixHD/fc_results \
--dataroot /research/dept7/glchen/datasets/dlsopc_datasets/fchdsep/via3/dmo \
--netG global \
--resize_or_crop none \
--name ovia3pixhd_e100_1024_dr2mg \
--loadSize 1024 \
--fineSize 1024 \
--which_epoch latest \
--how_many 10000 \
--norm instance \
--label_nc 0 \
--no_instance \
--zip_and_send \
--is_fc
