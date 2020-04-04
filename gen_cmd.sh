phase='train'
# phase='test'
# base config
# --------
for_good=true
# for_good=false
# --------
# user=glchen
# user=wlchen
user=xiaolin
# --------
# vianum=6
# vianum=5
vianum=4
# --------
n_layers_D=1
# --------
num_D=1
# --------
model='pix2pixHD'
# model='pix2pixL1'
# --------
load_crop_size=1024
# load_crop_size=512
# --------
train_set_num=2500
epoch=100
half_iter=`expr $epoch / 2`
p_freq=100

if [ $for_good = true ]; then
    dataroot='/research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via'$vianum'_good/dmo'
else
    dataroot='/research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via'$vianum'/dmo'
fi


##### test phases ####
# --------
test_epoch=latest
# test_epoch=100
# --------
test_num=500
# test_num=2000
# --------

if [ $model = "pix2pixHD" ]; then
    name='ovia'$vianum'pixhd'
elif [ $model = 'pix2pixLR' ]; then
    name='ovia'$vianum'pixlr'
elif [ $model = 'pix2pixL1' ]; then
    name='ovia'$vianum'pixl1'
else
    echo 'no model found'
fi

# if [ $load_crop_size = 1024 ]; then
#     resize_or_crop='none'
# else
#     resize_or_crop='resize_and_crop'
# fi

if [ $phase = "test" ]; then
    ext='.sh'
    gpu_num=1
else
    ext='.cmd'
    gpu_num=4
fi

# for training test
# ext='.sh'
# gpu_num=1

if [ $user = 'glchen' ]; then
    user_pre='gl'
elif [ $user = 'wlchen' ]; then
    user_pre='wl'
elif [ $user = 'xiaolin' ]; then
    user_pre='xl'
else
    echo 'no user found'
fi

if [ $for_good = true ]; then
    file_name=$user_pre'_'$phase'_'$name'_e'$epoch'_'$load_crop_size'_good_dr2mg'
else
    file_name=$user_pre'_'$phase'_'$name'_e'$epoch'_'$load_crop_size'_dr2mg'
fi

if [ $num_D != 2 ]; then
    file_name=$file_name'_D'$num_D
fi

if [ $n_layers_D != 3 ]; then
    file_name=$file_name'd'$n_layers_D
fi

echo $n_layers_D

file_name=$file_name$ext
echo $file_name

if [ $phase = "test" ]; then
    python gen_cmd.py \
--name $name \
--file_name $file_name \
--gpu_num $gpu_num \
--model $model \
--load_crop_size $load_crop_size \
--test_dmo \
--half_iter $half_iter \
--test_num $test_num \
--dataroot $dataroot \
--epoch $test_epoch \
--user $user

else
    python gen_cmd.py \
--name $name \
--file_name $file_name \
--gpu_num $gpu_num \
--load_crop_size $load_crop_size \
--model $model \
--half_iter $half_iter \
--dataroot $dataroot \
--user $user \
--train_set_num $train_set_num \
--p_freq $p_freq \
--num_D $num_D \
--n_layers_D $n_layers_D \
--vianum $vianum
fi

code $file_name

# --epoch $test_epoch \
