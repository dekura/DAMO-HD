###
 # @Author: Guojin Chen
 # @Date: 2020-04-13 09:44:13
 # @LastEditTime: 2020-05-12 23:13:04
 # @Contact: cgjhaha@qq.com
 # @Description: flow shell
###

python=/research/dept7/glchen/miniconda3/envs/gdspy/bin/python
# python=/usr/local/miniconda3/envs/gdspy/bin/python

$python flow.py \
--name ispd19fc5 \
--in_folder ./test_gds/ispd19test \
--max_via_in_win 5 \
--dmo_res_folder /research/dept7/glchen/datasets/gds/ispd19dmores
