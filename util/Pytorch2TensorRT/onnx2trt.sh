###
 # @Author: Guojin Chen @ CUHK-CSE
 # @Homepage: https://dekura.github.io/
 # @Date: 2021-02-27 10:26:14
 # @LastEditTime: 2021-02-27 10:41:33
 # @Contact: cgjhaha@qq.com
 # @Description: transfer the onnx model to the tensorRT engine
###

/research/d2/xfyao/tools/anaconda3/envs/maskrcnn/bin/python main.py \
--batch_size 1 \
--channel 3 \
--height 1024 \
--width 1024 \
--mode fp32 \
--onnx_file_path /research/d2/xfyao/guojin/pix2pixHD/onnx_model/dls_e100_d2m_fp32.onnx \
--engine_file_path /research/d2/xfyao/guojin/pix2pixHD/trt_engine/dls_e100_d2m_fp32.trt