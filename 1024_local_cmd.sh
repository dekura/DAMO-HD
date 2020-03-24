phase='train'
# phase='test'

name='ovia2pixhd'
dataroot='/research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via2/dmo'
load_crop_size=1024
model='pix2pixHD'
epoch=100
half_iter=`expr $epoch / 2`
pretrain='checkpoints/'$name'_e'$epoch'_512_dr2mg/'

# model='pix2pix'

p_freq=500

##### test phases ####
# test_epoch=80
test_num=1000

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


file_name=$phase'_'$name'_e'$epoch'_'$load_crop_size'_local_dr2mg'$ext
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
--pretrain_512 $pretrain

else
    python 1024_local_cmd.py \
--name $name \
--file_name $file_name \
--gpu_num $gpu_num \
--load_crop_size $load_crop_size \
--model $model \
--half_iter $half_iter \
--dataroot $dataroot \
--pretrain_512 $pretrain
fi

code $file_name

# --epoch $test_epoch \
