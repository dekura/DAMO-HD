# phase='train'
phase='test'
# base config
# --------
for_good=true
# for_good=false
# --------
user=glchen
# user=wlchen
# user=xiaolin
# --------
# vianum=6
# vianum=5
# vianum=4
# vianum=3
vianum=2
# vianum=1
# --------
# is_rect=false
is_rect=true
# --------
is_ispdrect=false
# is_ispdrect=true
# --------
n_layers_D=1
# --------
# num_D=1
num_D=2
# --------
# epoch=100
epoch=50
# --------
model='pix2pixHD'
# model='pix2pixL1'
# --------
load_crop_size=1024
# load_crop_size=512
# --------
save_epoch_freq=10
# --------
train_set_num=2000

half_iter=`expr $epoch / 2`
p_freq=100


##### test phases ####
# --------
test_epoch=latest
# test_epoch=100
# test_epoch=60
# --------
test_num=1000
# test_num=2000
# --------
# is_fc=true
is_fc=false
# --------
is_fc5=true
# is_fc5=false
# --------

if [ $is_rect = true ]; then
    root_folder='recthdsep'
else
    root_folder='viahdsep'
fi

if [ $is_ispdrect = true ]; then
    root_folder='ispdrecthdsep'
fi

fc_p=none
results_dir='results'

if [ $phase = "test" ]; then
    if [ $is_fc = true ]; then
        root_folder='fcrecthdsep'
        # for_good=false
        fc_p='_fc'
        results_dir='fc_results'
        test_num=10000
    fi

    if [ $is_fc5 = true ]; then
        root_folder='fc5recthdsep'
        # for_good=false
        fc_p='_fc5'
        results_dir='fc5_results'
        test_num=10000
    fi
fi



results_root='/research/dept7/glchen/github/pix2pixHD/'$results_dir

if [ $for_good = true ]; then
    dataroot='/research/dept7/glchen/datasets/dlsopc_datasets/'$root_folder'/via'$vianum'_good/dmo'
    if [ $phase = "test" ]; then
        if [[ $is_fc5 = true || $is_fc = true ]]; then
            dataroot='/research/dept7/glchen/datasets/dlsopc_datasets/'$root_folder'/via'$vianum'/dmo'
        fi
    fi
else
    dataroot='/research/dept7/glchen/datasets/dlsopc_datasets/'$root_folder'/via'$vianum'/dmo'
fi


if [ $is_rect = true ]; then
    rectname='orect'
else
    rectname='ovia'
fi

if [ $is_ispdrect = true ]; then
    rectname='oisrect'
fi

if [ $model = "pix2pixHD" ]; then
    name=$rectname$vianum'pixhd'
elif [ $model = 'pix2pixLR' ]; then
    name=$rectname$vianum'pixlr'
elif [ $model = 'pix2pixL1' ]; then
    name=$rectname$vianum'pixl1'
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


file_name=$file_name'_D'$num_D


if [ $n_layers_D != 3 ]; then
    file_name=$file_name'd'$n_layers_D
fi

echo $n_layers_D

if [[ $fc_p != none ]]; then
    file_name=$file_name$fc_p
fi

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
--user $user \
--num_D $num_D \
--n_layers_D $n_layers_D \
--vianum $vianum \
--fc_p $fc_p \
--results_root $results_root

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
--vianum $vianum \
--save_epoch_freq $save_epoch_freq
fi

code $file_name

# --epoch $test_epoch \
