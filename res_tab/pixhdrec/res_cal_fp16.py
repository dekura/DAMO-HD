'''
Author: Guojin Chen @ CUHK-CSE
Homepage: https://dekura.github.io/
Date: 2021-03-01 15:44:01
LastEditTime: 2021-03-05 10:26:24
Contact: cgjhaha@qq.com
Description: the results cal.
'''
import numpy as np


acce_r = 0.55

iccad_t = np.array([284, 281, 285, 291, 279, 284])

tcad_t = iccad_t * acce_r

ispd_t = np.array([3669, 1591, 949, 313, 466])

tcad_ispd_t = ispd_t * acce_r

tcad_l2 = np.array([1086, 2153, 3296, 4311, 5405, 6511])

tcad_pvb = np.array([2922, 5563, 8265, 10931, 13627, 15536])

tcad_t = np.array([185, 183, 185, 190, 183, 184])

tcad_avgs = np.array([np.mean(tcad_l2), np.mean(tcad_pvb), np.mean(tcad_t)])
tcad_rates = [np.mean(tcad_l2)/3682 , np.mean(tcad_pvb)/9482, np.mean(tcad_t)/284]


tcad_ispd_l2 = np.array([1070, 2217, 3329, 4387, 4923])
tcad_ispd_pvb = np.array([2850, 5666, 8173, 11014, 12279])
tcad_ispd_t = np.array([2498, 1029, 674, 244, 315])

tcad_ispd_avgs = np.array([np.mean(tcad_ispd_l2), np.mean(tcad_ispd_pvb), np.mean(tcad_ispd_t)])
tcad_ispd_rates = [np.mean(tcad_ispd_l2)/3065 , np.mean(tcad_ispd_pvb)/7973, np.mean(tcad_ispd_t)/1397]



print('tcad avgs: ', tcad_avgs)
print('tcad rates: ',tcad_rates)

print('tcad_ispd avgs: ', tcad_ispd_avgs)
print('tcad_ispd rates: ',tcad_ispd_rates)
# print(tcad_t)
# print(tcad_ispd_t)
