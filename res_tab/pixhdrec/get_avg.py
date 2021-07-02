'''
Author: Guojin Chen @ CUHK-CSE
Homepage: https://dekura.github.io/
Date: 2021-07-02 14:26:53
LastEditTime: 2021-07-02 14:53:19
Contact: cgjhaha@qq.com
Description: get the average scores
'''
import numpy as np

# data for validataion

# l2 = [1075, 2121, 3207, 4225, 5344, 5913]
# pvb = [2909, 5562, 8254, 10917, 13611, 15497]
# rt = [203, 199, 205, 204, 198, 201]

# data for ispd
l2 = [1049, 2149, 3110, 4298, 4465]
pvb = [2841, 5617, 8067, 10817, 12097]
rt = [2688, 1151, 694, 228, 335]



l2 = np.array(l2)
pvb = np.array(pvb)
rt = np.array(rt)

l2_m = np.mean(l2)
pvb_m = np.mean(pvb)
rt_m = np.mean(rt)
print(l2_m)
print(pvb_m)
print(rt_m)

# l2_damo = 3682
# pvb_damo = 9482
# rt_damo = 284

# for ispd
l2_damo = 3065
pvb_damo = 7973
rt_damo = 1397

l2_r = l2_m / l2_damo
pvb_r = pvb_m / pvb_damo
rt_r = rt_m / rt_damo

print(l2_r)
print(pvb_r)
print(rt_r)