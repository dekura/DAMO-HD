'''
@Author: Guojin Chen
@Date: 2020-05-05 08:58:14
@LastEditTime: 2020-05-05 10:57:08
@Contact: cgjhaha@qq.com
@Description: l2 loss test
'''


import os
import time
import torch
from tqdm import tqdm
import numpy as np
from options.test_options import TestOptions
from data.data_loader import CreateDataLoader

opt = TestOptions().parse(save=False)
opt.nThreads = 1   # test code only supports nThreads = 1
opt.batchSize = 1  # test code only supports batchSize = 1
opt.serial_batches = True  # no shuffle
opt.no_flip = True  # no flip

data_loader = CreateDataLoader(opt)
dataset = data_loader.load_data()
# create website
# web_dir = os.path.join(opt.results_dir, opt.name, '%s_%s' % (opt.phase, opt.which_epoch))
web_dir = os.path.join(opt.results_dir, opt.name)  # define the website directory
if not os.path.exists(web_dir):
    os.mkdir(web_dir)
txt_path = web_dir + '/{}_epoch_{}.txt'.format(opt.name,opt.which_epoch)
l2_txt_path = web_dir + '/{}_epoch_{}_l2loss.txt'.format(opt.name,opt.which_epoch)

RED_LAYER = 0
GREEN_LAYER = 1

def save_result2txt(path, l2loss, std, running_time):
    f = open(path,'a+')
    f.write('testing time : {} \n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    f.write('total running time: {}\n'.format(running_time))
    f.write('l2loss: {} \n'.format(l2loss))
    f.write('std: {} \n'.format(std))
    f.close()
# test
tbar = tqdm(dataset)
opt.how_many = min(opt.how_many, len(tbar))
finalAcc , finalmIoU = 0, 0
l2loss_mean = 0
std = 0
l2loss_arr = []
t = time.time()

for i, data in enumerate(tbar):
    if i >= opt.how_many:
        break
    if opt.data_type == 16:
        data['label'] = data['label'].half()
        data['inst']  = data['inst'].half()
    elif opt.data_type == 8:
        data['label'] = data['label'].uint8()
        data['inst']  = data['inst'].uint8()
    minibatch = 1
    img_path = data['path']
    wafer = data['image'][0]
    wafer = (wafer + 1)/2
    wafer = wafer[RED_LAYER]

    design = data['label'][0]
    design = (design + 1)/2
    design = design[RED_LAYER]

    before_sum = l2loss_mean * i
    l2_loss = torch.nn.MSELoss(reduction='sum')(wafer, design)
    now_sum = before_sum + l2_loss
    l2loss_mean = now_sum/(i+1)
    l2loss_arr.append(l2_loss)
    l2loss_arr_np = np.array(l2loss_arr)
    std = np.nanstd(l2loss_arr_np, ddof=1)
    tbar.set_description('l2loss: %.4f, std: %.4f' % (l2loss_mean, std))
elapsed = time.time() - t
np.savetxt(l2_txt_path, np.array(l2loss_arr))
print('total running time: {}'.format(elapsed))
save_result2txt(txt_path, l2loss_mean, std, elapsed)


