###
# @Author: Guojin Chen
 # @Date: 2019-11-14 14:04:27
 # @LastEditTime: 2019-11-17 01:22:30
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


rm -rf ./test_gds/*
mkdir ./test_gds/$name
# cp -r /Users/dekura/chen/py/design_mask2gds_2048_512/out_lb/ ./test_gds
cp /Users/dekura/chen/py/design_mask2gds_2048_1024/gds/via7_rgb.gds ./test_gds/$name/
cp /Users/dekura/chen/py/design_mask2gds_2048_1024/gds/via5_rgb.gds ./test_gds/$name/
cp /Users/dekura/chen/py/design_mask2gds_2048_1024/gds/via8_rgb.gds ./test_gds/$name/



scp -r ./test_gds/$name calibre:/home/glchen/epetest_1024/test_gds/