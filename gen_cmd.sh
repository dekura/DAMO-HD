phase='train'
# phase='test'

# base config
vianum=2
name='ovia'$vianum'pixhd'
dataroot='/research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via'$vianum'/dmo'
load_crop_size=512
model='pix2pixHD'
epoch=100
half_iter=`expr $epoch / 2`
p_freq=500


##### test phases ####
# test_epoch=100
# test_num=10

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
# gpu_num=4

file_name=$phase'_'$name'_e'$epoch'_'$load_crop_size'_dr2mg'$ext
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
--epoch $test_epoch

else
    python gen_cmd.py \
--name $name \
--file_name $file_name \
--gpu_num $gpu_num \
--load_crop_size $load_crop_size \
--model $model \
--half_iter $half_iter \
--dataroot $dataroot
fi

code $file_name

# --epoch $test_epoch \
