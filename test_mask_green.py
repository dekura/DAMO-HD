import os
import time
import torch
import tarfile
import shutil
from util import html
from tqdm import tqdm
import util.util as util
from collections import OrderedDict
from torch.autograd import Variable
from models.models import create_model
from util.visualizer import Visualizer
from options.test_options import TestOptions
from data.data_loader import CreateDataLoader
from util.metrics import SegmentationMetric

opt = TestOptions().parse(save=False)
opt.nThreads = 1   # test code only supports nThreads = 1
opt.batchSize = 1  # test code only supports batchSize = 1
opt.serial_batches = True  # no shuffle
opt.no_flip = True  # no flip

data_loader = CreateDataLoader(opt)
dataset = data_loader.load_data()
visualizer = Visualizer(opt)
# create website
web_dir = os.path.join(opt.results_dir, opt.name, '%s_%s' % (opt.phase, opt.which_epoch))
webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.which_epoch))
txt_path = web_dir + '/{}_epoch_{}.txt'.format(opt.name,opt.which_epoch)
metric = SegmentationMetric(2)

GREEN_LAYER = 1

def save_result2txt(path, pixAcc, mIoU, running_time):
    f = open(path,'a+')
    f.write('testing time : {} \n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    f.write('total running time: {}\n'.format(running_time))
    f.write('pixAcc: {}, mIoU: {} \n \n'.format(pixAcc,mIoU))
    f.close()

# test
if not opt.engine and not opt.onnx:
    model = create_model(opt)
    if opt.data_type == 16:
        model.half()
    elif opt.data_type == 8:
        model.type(torch.uint8)
    if opt.verbose:
        print(model)
else:
    from run_engine import run_trt_engine, run_onnx


tbar = tqdm(dataset)
opt.how_many = min(opt.how_many, len(tbar))
finalAcc , finalmIoU = 0, 0
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
    if opt.export_onnx:
        print ("Exporting to ONNX: ", opt.export_onnx)
        assert opt.export_onnx.endswith("onnx"), "Export model file should end with .onnx"
        torch.onnx.export(model, [data['label'], data['inst']],
                            opt.export_onnx, verbose=True)
        exit(0)
    minibatch = 1
    if opt.engine:
        generated = run_trt_engine(opt.engine, minibatch, [data['label'], data['inst']])
    elif opt.onnx:
        generated = run_onnx(opt.onnx, opt.data_type, minibatch, [data['label'], data['inst']])
    else:
        generated = model.inference(data['label'], data['inst'], data['image'])

    # visuals = OrderedDict([('input_label', util.tensor2label(data['label'][0], opt.label_nc)),
    # ('synthesized_image', util.tensor2im(generated.data[0]))])
    # print(data)
    # print(data['label'].size())
    # print(data['image'].size())
    # print(generated.data.size())
    visuals = OrderedDict([('input_label', util.tensor2label(data['label'][0], opt.label_nc)),
                        ('synthesized_image', util.tensor2im(generated.data[0])),
                        ('real_image', util.tensor2im(data['image'][0]))])
    img_path = data['path']

    gnd = data['image'][0].cpu().numpy()
    gnd = (gnd + 1)/2
    gnd = gnd[GREEN_LAYER]

    pred = generated.data[0].cpu().numpy()
    pred = (pred + 1)/2
    pred = pred[GREEN_LAYER]

    metric.update(gnd, pred)
    acc_cls, mean_iu = metric.get()
    tbar.set_description('pixAcc: %.4f, mIoU: %.4f' % (acc_cls, mean_iu))
    if i == opt.how_many - 1:
        finalAcc = acc_cls
        finalmIoU = mean_iu

    # print('process image... %s' % img_path)
    visualizer.save_images(webpage, visuals, img_path)

elapsed = time.time() - t
webpage.save()
print('total running time: {}'.format(elapsed))
save_result2txt(txt_path, finalAcc, finalmIoU, elapsed)


#一次性打包整个根目录。空子目录会被打包。
#如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
def make_targz(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

if opt.is_fc:
    fc_p = opt.fc_p
    res_dir_name = os.path.join(opt.results_dir, opt.name)
    res_dir_name_fc = os.path.join(opt.results_dir, opt.name+fc_p)
    os.rename(res_dir_name, res_dir_name_fc)
    opt.name = opt.name+fc_p

if opt.zip_and_send:
    res_dir = os.path.join(opt.results_dir, opt.name)
    tarname = os.path.join(opt.results_dir, '{}.tar.gz'.format(opt.name))

    # scp testbg
    testbgtar = os.path.join(res_dir, 'testbg.tar.gz')
    if not os.path.exists(testbgtar):
        testbgtarsrc = os.path.join(opt.dataroot, 'testbg.tar.gz')
        shutil.copyfile(testbgtarsrc, testbgtar)
        testbg = tarfile.open(testbgtar)
        testbg.extractall(path=res_dir)

    make_targz(tarname, res_dir)
    os.system('bash ~/bin/scpdmo.sh {}'.format(tarname))