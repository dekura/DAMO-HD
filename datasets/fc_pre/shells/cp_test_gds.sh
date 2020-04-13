###
# @Author: Guojin Chen
 # @Date: 2019-11-14 14:04:27
 # @LastEditTime: 2019-11-25 10:08:11
 # @Contact: cgjhaha@qq.com
 # @Description: this get gds from test folder
 ###
name=$1

if [ ! -n "$1" ] ;then
    echo "you have not input a name!"
    exit 2
else
    echo "the word you input is $1"
fi


# cp -r /home/glchen/design_mask2gds/design_mask2gds_2048_1024/gds /home/glchen/epetest_1024/test_gds/$name

# cp -r /home/glchen/design_mask2gds/design_mask2gds_mt/gds/dcupp_naive6_weighted_100epoch_dr2mg_2048_2048_uppscale4 /home/glchen/epetest_mt/test_gds/$name


# cp -r /home/glchen/design_mask2gds/design_mask2gds_mt/gds/newdcupp_naive6_100epoch_dr2mg_2048_1024_50epoch /home/glchen/epetest_mt/test_gds/$name

# cp -r /home/glchen/design_mask2gds/design_mask2gds_mt/gds/gan2gan_100epoch_2048_1024_gl_sl1_fixed_50epoch /home/glchen/epetest_mt/test_gds/$name

# cp -r /home/glchen/design_mask2gds/design_mask2gds_mt/gds/gan2gan_100epoch_2048_1024_gl_sl1_fixed_100epoch /home/glchen/epetest_mt/test_gds/$name
cp -r /home/glchen/design_mask2gds/design_mask2gds_mt/gds/via1_10_100epoch_gds /home/glchen/epetest_mt/test_gds/$name