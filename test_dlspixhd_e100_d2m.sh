/research/d2/xfyao/tools/anaconda3/envs/maskrcnn/bin/python test.py \
--gpu_ids 0 \
--checkpoints_dir /research/d2/xfyao/guojin/pix2pixHD/checkpoints \
--results_dir /research/d2/xfyao/guojin/pix2pixHD/results \
--dataroot /research/d2/xfyao/guojin/data/datasets/develset/ \
--model pix2pixHD \
--netG global \
--resize_or_crop resize_and_crop \
--loadSize 1024 \
--fineSize 1024 \
--name dls_e100_d2m \
--which_epoch latest \
--how_many 1000 \
--norm batch \
--label_nc 0 \
--no_instance
