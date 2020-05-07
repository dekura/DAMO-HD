###
 # @Author: Guojin Chen
 # @Date: 2020-04-15 09:11:04
 # @LastEditTime: 2020-05-05 10:38:25
 # @Contact: cgjhaha@qq.com
 # @Description: gen fc images
###
python=/research/dept7/glchen/miniconda3/envs/guojin/bin/python

name=fc5recthdsep

$python flow.py \
--name $name \
--load_size 2048 \
--crop_size 1024 \
--gen_only_fc \
--max_pervia 10000 \
--for_dmo \
--set_byvia \
--gen_via_lists 1,2,3,4,5,6 \
--gds_path /research/dept7/glchen/github/pix2pixHD/datasets/fc_pre/results/ispd19fc5 \
--out_folder /research/dept7/glchen/datasets/dlsopc_datasets/$name
