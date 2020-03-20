phase='train'
# phase='test'

name='ovia2pixhd'
dataroot='/research/dept7/glchen/datasets/dlsopc_datasets/viahdsep/via2/dmo'

# model='pix2pix'
model='pix2pixHD'

epoch=100
half_iter=`expr $epoch / 2`
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


file_name=$phase'_'$name'_e'$epoch'_dr2mg'$ext
echo $file_name

if [ $phase = "test" ]; then
    python gen_cmd.py \
--name $name \
--file_name $file_name \
--gpu_num $gpu_num \
--model $model \
--test_dmo \
--half_iter $half_iter \
--test_num $test_num \
--dataroot $dataroot

else
    python gen_cmd.py \
--name $name \
--file_name $file_name \
--gpu_num $gpu_num \
--model $model \
--half_iter $half_iter \
--dataroot $dataroot
fi

code $file_name

# --epoch $test_epoch \
