###
 # @Author: Guojin Chen
 # @Date: 2020-05-05 09:44:05
 # @LastEditTime: 2020-05-05 20:13:02
 # @Contact: cgjhaha@qq.com
 # @Description: flow to test l2 loss
###
python=/research/dept7/glchen/miniconda3/envs/guojin/bin/python

# gds_folder_name=pix2l2gds
name=orect5pixhd_e100_1024_good_dr2mg_D2d1_fc5
out_folder=pix2l2rect

$python flow.py \
--name $name \
--load_size 2048 \
--crop_size 1024 \
--max_pervia 10000 \
--for_dls \
--gen_only_l2 \
--gds_path /research/dept7/glchen/datasets/dlsopc_datasets/pix2l2gds/$name/gds \
--gds_post '*_GAN.gds' \
--out_folder /research/dept7/glchen/datasets/dlsopc_datasets/$out_folder/$name


$python flow.py \
--name $name \
--load_size 2048 \
--crop_size 1024 \
--max_pervia 10000 \
--for_dls \
--gen_only_l2 \
--gds_path /research/dept7/glchen/datasets/dlsopc_datasets/pix2l2gds/$name/gds \
--gds_post '*_CALI.gds' \
--out_folder /research/dept7/glchen/datasets/dlsopc_datasets/$out_folder/$name'_CALI'
