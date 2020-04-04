# phase='train'
phase='test'

# base config
# --------
user=glchen
# user=wlchen
# user=xiaolin
# --------
# vianum=6
# vianum=5
# vianum=4
vianum=2
# --------
model='pix2pixHD'
# --------
load_crop_size=1024
# load_crop_size=512
# --------
train_set_num=2500
dataroot='/research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via'$vianum'/dmo'
epoch=100
half_iter=`expr $epoch / 2`
p_freq=100

##### test phases ####
test_epoch=latest
test_num=2000

if [ $model = "pix2pixHD" ]; then
    name='ovia'$vianum'pixhd'
elif [ $model = 'pix2pixLR' ]; then
    name='ovia'$vianum'pixlr'
else
    echo 'no model found'
fi

pretrain='checkpoints/'$name'_e'$epoch'_512_dr2mg/'

if [ $phase = "test" ]; then
    ext='.sh'
    gpu_num=1
else
    ext='.cmd'
    gpu_num=4
fi

# for training test
# ext='.sh'
# gpu_num=4

if [ $user = 'glchen' ]; then
    user_pre='gl'
elif [ $user = 'wlchen' ]; then
    user_pre='wl'
elif [ $user = 'xiaolin' ]; then
    user_pre='xl'
else
    echo 'no user found'
fi


file_name=$user_pre'_'$phase'_'$name'_e'$epoch'_'$load_crop_size'_local_dr2mg'$ext

echo $file_name

if [ $phase = "test" ]; then
    python 1024_local_cmd.py \
--name $name \
--file_name $file_name \
--gpu_num $gpu_num \
--model $model \
--load_crop_size $load_crop_size \
--test_dmo \
--half_iter $half_iter \
--test_num $test_num \
--dataroot $dataroot \
--pretrain_512 $pretrain \
--epoch $test_epoch \
--user $user

else
    python 1024_local_cmd.py \
--name $name \
--file_name $file_name \
--gpu_num $gpu_num \
--load_crop_size $load_crop_size \
--model $model \
--half_iter $half_iter \
--dataroot $dataroot \
--pretrain_512 $pretrain \
--user $user \
--train_set_num $train_set_num
fi

code $file_name

# --epoch $test_epoch \
