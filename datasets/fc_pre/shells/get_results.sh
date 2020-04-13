### 
# @Author: Guojin Chen
 # @Date: 2019-11-14 14:12:08
 # @LastEditTime: 2019-11-18 16:28:11
 # @Contact: cgjhaha@qq.com
 # @Description: get results from server
 ###

name=$1

if [ ! -n "$1" ] ;then
    echo "you have not input a name!"
    exit 2
else
    echo "the word you input is $1"
fi

scp -r calibre:/home/glchen/epetest_1024/results/$name ./results

open ./results

