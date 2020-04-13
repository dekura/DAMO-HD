'''
@Author: Guojin Chen
@Date: 2020-04-10 11:45:19
@LastEditTime: 2020-04-10 14:58:46
@Contact: cgjhaha@qq.com
@Description: cali merge rule
'''
def cali_merge_rule(gds_path, out_gds_path):
    drc_code = """
LAYOUT PATH    '%s'
""" % (gds_path)
    drc_code += """
LAYOUT PRIMARY '*'
"""
    drc_code += """
DRC RESULTS DATABASE '%s' GDSII
""" % (out_gds_path)
    drc_code += """
PRECISION 1000
LAYOUT SYSTEM GDSII
DRC MAXIMUM RESULTS ALL
DRC MAXIMUM VERTEX 4000

LAYER MAP 0   datatype 0 1000 LAYER target     1000
LAYER MAP 1   datatype 0 1001 LAYER opc        1001
LAYER MAP 2   datatype 0 1002 LAYER sraf       1002
LAYER MAP 400   datatype 0 1003 LAYER merge_layer       1003
// LAYER MAP 600   datatype 0 1004 LAYER bbox       1004
// LAYER MAP 50  datatype 0 1003 LAYER lay_gangt  1003

// #01: output results
// out_sraf = NOT lay_bbox lay_nosraf
OUT_target     {COPY target     } DRC CHECK MAP OUT_target    0      0
OUT_opc        {COPY opc        } DRC CHECK MAP OUT_opc       1      0
OUT_sraf       {COPY sraf       } DRC CHECK MAP OUT_sraf      2      0
OUT_merge      {COPY merge_layer      } DRC CHECK MAP OUT_merge     400    0
"""
    return drc_code