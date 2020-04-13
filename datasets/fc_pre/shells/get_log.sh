### 
# @Author: Guojin Chen
 # @Date: 2019-11-14 14:12:08
 # @LastEditTime: 2019-11-26 19:09:43
 # @Contact: cgjhaha@qq.com
 # @Description: get resultes from server
 ###

rm -rf './log/*'

mkdir './log/test_pvband'
# scp -r calibre:/home/glchen/epetest_1024/sqldb/* ./sqldb

scp -r calibre:/home/glchen/pvband_mt/log/test_pvband/* ./log/test_pvband/



