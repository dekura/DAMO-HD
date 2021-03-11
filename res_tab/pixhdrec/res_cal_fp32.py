'''
Author: Guojin Chen @ CUHK-CSE
Homepage: https://dekura.github.io/
Date: 2021-03-01 15:44:01
LastEditTime: 2021-03-05 11:09:11
Contact: cgjhaha@qq.com
Description: the results cal.
'''
import numpy as np


acce_r = 0.73

iccad_t = np.array([284, 281, 285, 291, 279, 284])

tcad_t = iccad_t * acce_r

ispd_t = np.array([3669, 1591, 949, 313, 466])

tcad_ispd_t = ispd_t * acce_r

print('tcad_t: ', tcad_t)
print('tcad_ispd_t: ', tcad_ispd_t)

tcad_l2 = np.array([1081, 2129, 3244, 4263, 5397, 5982])


tcad_pvb = np.array([2916, 5574, 8271, 10946, 13640, 15542])

tcad_t = np.array([203, 199, 205, 204, 198, 201])

tcad_avgs = np.array([np.mean(tcad_l2), np.mean(tcad_pvb), np.mean(tcad_t)])
tcad_rates = [np.mean(tcad_l2)/3682 , np.mean(tcad_pvb)/9482, np.mean(tcad_t)/284]


tcad_ispd_l2 = np.array([1056, 2172, 3196, 4362, 4542])
tcad_ispd_pvb = np.array([2848, 5654, 8127, 10987, 12250])
tcad_ispd_t = np.array([2688, 1151, 694, 228, 335])

tcad_ispd_avgs = np.array([np.mean(tcad_ispd_l2), np.mean(tcad_ispd_pvb), np.mean(tcad_ispd_t)])
tcad_ispd_rates = [np.mean(tcad_ispd_l2)/3065 , np.mean(tcad_ispd_pvb)/7973, np.mean(tcad_ispd_t)/1397]



print('tcad avgs: ', tcad_avgs)
print('tcad rates: ',tcad_rates)

print('tcad_ispd avgs: ', tcad_ispd_avgs)
print('tcad_ispd rates: ',tcad_ispd_rates)
# # print(tcad_t)
# print(tcad_ispd_t)
