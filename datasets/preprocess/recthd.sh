###
 # @Author: Guojin Chen
 # @Date: 2020-04-25 10:38:25
 # @LastEditTime: 2020-04-27 14:39:51
 # @Contact: cgjhaha@qq.com
 # @Description: gen rect hd sep
###

# remote server
python=/research/dept7/glchen/miniconda3/envs/guojin/bin/python

name=recthdsep
vianum=3

$python flow.py \
--name $name \
--load_size 2048 \
--crop_size 1024 \
--test_ratio 4 \
--max_pervia 2000 \
--for_dmo \
--set_byvia \
--gen_via_lists $vianum \
--gen_seen_set \
--gds_path /research/dept7/glchen/datasets/gds/ovia$vianum/gds/ \
--out_folder /research/dept7/glchen/datasets/dlsopc_datasets/$name \
# --gen_good \
# --sqldb_path /research/dept7/glchen/proj12/ovia$vianum.db \
# --epebar 0.7
