###
 # @Author: Guojin Chen
 # @Date: 2020-04-13 09:44:13
 # @LastEditTime: 2021-08-09 14:54:45
 # @Contact: cgjhaha@qq.com
 # @Description: flow shell
###

# python=/research/dept7/glchen/miniconda3/envs/gdspy/bin/python
# python=/usr/local/miniconda3/envs/gdspy/bin/python
python=/home/glchen/miniconda3/envs/gdspy/bin/python

# $python flow.py \
# --name ispd19fc5 \
# --in_folder ./test_gds/ispd19test \
# --max_via_in_win 5 \
# --dmo_res_folder /home/glchen/datasets/ispd19dmores
# --dmo_res_folder /research/dept7/glchen/datasets/gds/ispd19dmores

$python flow.py \
--name ispd19test \
--in_folder ./test_gds/ispd19test \
--max_via_in_win 5 \
--dmo_res_folder /home/glchen/datasets/ispd19dmores