python=/home/guojin/miniconda3/envs/pixhd/bin/python
$python test_mask_green.py \
--gpu_ids 0 \
--checkpoints_dir ./checkpoints \
--results_dir ./results \
--dataroot /home/guojin/data/datasets/pix2pixHD/develset \
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
--no_instance \
--onnx ./onnx_model/dls_e100_d2m_fp32.onnx