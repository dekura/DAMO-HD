### 
# @Author: Guojin Chen
 # @Date: 2019-11-14 14:12:08
 # @LastEditTime: 2019-11-26 23:34:28
 # @Contact: cgjhaha@qq.com
 # @Description: get resultes from server
 ###

# rm -rf './epedb/*'
# mkdir ./sqldb/test_pvband
# scp -r calibre:/home/glchen/pvband_mt/sqldb/test_pvband/* ./sqldb/test_pvband/
mkdir ./sqldb/ganopc_upp_base_25epoch
scp -r calibre:/home/glchen/pvband_mt/sqldb/ganopc_upp_base_25epoch/ganopc_upp_base_25epoch.db ./sqldb/ganopc_upp_base_25epoch/

open ./sqldb