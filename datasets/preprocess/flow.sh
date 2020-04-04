# remote server
python=/research/dept7/glchen/miniconda3/envs/guojin/bin/python

vianum=6

$python flow.py \
--name viahdsep \
--load_size 2048 \
--crop_size 1024 \
--test_ratio 4 \
--max_pervia 5000 \
--for_dmo \
--for_dls \
--set_byvia \
--gen_via_lists $vianum \
--gen_seen_set \
--gds_path '/research/dept7/glchen/datasets/gds/ovia'$vianum'/gds/' \
--out_folder /research/dept7/glchen/datasets/dlsopc_datasets/viahdsep \
--gen_good \
--sqldb_path '/research/dept7/glchen/proj12/ovia'$vianum'.db' \
--epebar 0.6


# one more thing to compress the testbg

# local test


# python=/usr/local/miniconda3/envs/pytorch/bin/python
# $python flow.py \
# --name testforhd \
# --load_size 2048 \
# --crop_size 1024 \
# --for_dmo \
# --for_dls \
# --set_byvia \
# --gen_via_lists 2 \
# --gds_path /Users/dekura/Downloads/testforpredataset/ \
# --out_folder /Users/dekura/Downloads/testforhd/