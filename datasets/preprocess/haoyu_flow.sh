# remote server
python=/research/d4/gds/gjchen21/miniconda3/envs/torch1.2/bin/python


name=ispdhaoyusep

$python flow.py \
--name $name \
--load_size 1024 \
--crop_size 1024 \
--test_ratio 1 \
--max_pervia 2000 \
--for_dmo \
--for_dls
# --gen_seen_set \
--gds_path /research/dept7/glchen/github/pix2pixHD/datasets/fc_pre/results/ispd19fc5 \
--out_folder /research/dept7/glchen/datasets/dlsopc_datasets/$name

# --gds_path /research/dept7/glchen/datasets/gds/layouts05frac48via12/gds/ \
# --out_folder /research/dept7/glchen/datasets/dlsopc_datasets/recthdsep


# --gen_good \
# --sqldb_path '/research/dept7/glchen/proj12/ovia'$vianum'.db' \
# --epebar 0.7

# $python flow.py \
# --name viahdsep \
# --load_size 2048 \
# --crop_size 1024 \
# --test_ratio 4 \
# --max_pervia 5000 \
# --for_dmo \
# --for_dls \
# --set_byvia \
# --gen_via_lists $vianum \
# --gen_seen_set \
# --gds_path '/research/dept7/glchen/datasets/gds/layouts05frac48via12/gds/' \
# --out_folder /research/dept7/glchen/datasets/dlsopc_datasets/viahdsep \
# --gen_good \
# --sqldb_path '/research/dept7/glchen/proj12/layouts05frac48via12t9.db' \
# --epebar 0.7




# one more thing to compress the testbg

# local test


# python=/usr/local/miniconda3/envs/pytorch/bin/python
# $python flow.py \
# --name testforhd \
# --load_size 2048 \
# --crop_size 1024 \
# --for_dmo \
# --set_byvia \
# --gen_via_lists 1 \
# --gds_path /Users/dekura/Downloads/testforpredataset/ \
# --out_folder /Users/dekura/Downloads/testforhd/