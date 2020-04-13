###
# @Author: Guojin Chen
 # @Date: 2019-11-14 14:04:27
 # @LastEditTime: 2019-11-17 01:24:00
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


rm -rf ./converted_oas/*.oas
rm -rf ./results/*.oas
rm -rf ./results/*/*.oas
rm -rf ./test_gds/*.gds
rm -rf ./test_gds/*.oas
rm -rf ./test_gds/*/*.gds
rm -rf ./test_gds/*/*.oas

echo "all folder cleaned"



rm -rf ./test_gds/*

# cp -r /Users/dekura/chen/py/design_mask2gds_2048_512/gds/ ./test_gds/$name

# scp -r /Users/dekura/chen/py/design_mask2gds_2048_512/gds/ calibre:/home/glchen/epetest_1024/test_gds/$name
cp -r /home/glchen/design_mask2gds_2048_1024/gds/ /home/glchen/epetest_1024/test_gds/$name