###
# @Author: Guojin Chen
# @Date: 2019-11-14 13:58:56
 # @LastEditTime: 2019-11-17 01:26:16
# @Contact: cgjhaha@qq.com
# @Description: this file clean folder before you run,
#    it is more convinient to test
###


rm -rf ./converted_oas/*.oas
rm -rf ./results/*.oas
rm -rf ./results/*/*.oas
rm -rf ./test_gds/*.gds
rm -rf ./test_gds/*.oas
rm -rf ./test_gds/*/*.gds
rm -rf ./test_gds/*/*.oas


echo "all folder cleaned"