'''
@Author: Guojin Chen
@Date: 2020-04-12 09:02:31
@LastEditTime: 2020-05-12 13:55:28
@Contact: cgjhaha@qq.com
@Description: class of shapes
'''

import numpy as np
from const import MERGE_WH, VIA_WH, PRECISION, VIA_WIN_WH

# xl = poly[0][0]  # 25
# xr = poly[1][0]  # 75
# yd = poly[0][1]  # 25
# yu = poly[2][1]  # 75

# def check_center_in_vias(opc_centers, via_center):

def poly_to_rect(poly):
    xl = poly[0][0]  # 25
    xr = poly[1][0]  # 75
    yd = poly[0][1]  # 25
    yu = poly[2][1]  # 75
    point1 = np.array([xl, yd])
    point2 = np.array([xr, yu])
    return (point1, point2)

def center_to_rect(center):
    xl = center[0] - (VIA_WH/2)/PRECISION
    xr = xl + VIA_WH/PRECISION
    yd = center[1] - (VIA_WH/2)/PRECISION
    yu = yd + VIA_WH/PRECISION
    point1 = np.array([xl, yd])
    point2 = np.array([xr, yu])
    return (point1, point2)

class FINAL_RECT:
    'the final cut rect'
    def __init__(self, center, vias):
        center = np.around(center, decimals=3)
        self.center = center
        self.left = center[0] - (VIA_WIN_WH/2)/PRECISION
        self.right = self.left + VIA_WIN_WH/PRECISION
        self.down = center[1] - (VIA_WIN_WH/2)/PRECISION
        self.up = self.down + VIA_WIN_WH/PRECISION
        point1 = np.array([self.left, self.down])
        point2 = np.array([self.right, self.up])
        self.rect = (point1, point2)
        # self.via_rects = []
        self.vias = vias
        self.opc_rects = []
        self.sraf_rects = []
        # self.via_center2rects()

    def via_center2rects(self):
        via_rects = []
        for center in self.vias:
            rect = center_to_rect(center)
            via_rects.append(rect)
        # self.via_rects = via_rects
        return via_rects

    def get_opc_rects(self, opc_polys, opc_centers):
        dis = (VIA_WH/2)/PRECISION
        opc_rects = []
        for index, center in enumerate(self.vias):
            pos = np.where((np.abs(center[0] - opc_centers[:, 0]) <= dis) & (np.abs(center[1] - opc_centers[:, 1]) <= dis))
            opc_poly = opc_polys[pos]
            # print('via center: ', self.vias[index])
            # print('opc center: ', opc_centers[pos])
            opc_rect = poly_to_rect(opc_poly[0])
            opc_rects.append(opc_rect)
        self.opc_rects = opc_rects
        assert len(self.opc_rects) == len(self.vias)

    def get_sraf_rects(self, sraf_polys, sraf_centers):
        sraf_win_wh = self.get_sraf_win_wh()
        left = self.center[0] - (sraf_win_wh/2)/PRECISION
        right = left + sraf_win_wh/PRECISION
        down = self.center[1] - (sraf_win_wh/2)/PRECISION
        up = down + sraf_win_wh/PRECISION
        pos = np.where((sraf_centers[:, 0] > left) & (sraf_centers[:, 0] < right) &
        (sraf_centers[:, 1] > down) & (sraf_centers[:, 1] < up))
        polys = sraf_polys[pos]
        sraf_rects = []
        for poly in polys:
            sraf_rect = poly_to_rect(poly)
            sraf_rects.append(sraf_rect)
        self.sraf_rects = sraf_rects
        # print('via {} sraf {}'.format(len(self.vias), len(self.sraf_rects)))


    def get_sraf_win_wh(self):
        via_num = len(self.vias)
        if via_num <= 3 :
            return 1300

        if via_num <= 6:
            return 1800


class MERGE_RECT:
    'all merge_rect belong to this class'
    def __init__(self, rect_poly):
        self.poly = rect_poly
        self.left = self.get_margin('left')
        self.right = self.get_margin('right')
        self.up = self.get_margin('up')
        self.down = self.get_margin('down')
        point1 = np.array([self.left, self.down])
        point2 = np.array([self.right, self.up])
        self.rect = (point1, point2)
        self.center = np.array([(self.left +  self.right)/2, (self.up+ self.down)/2])
        self.vias = []

    def get_margin(self, direction):
        poly_np = np.array(self.poly)
        if direction == 'left':
            xl = np.min(poly_np[:, 0])
            return xl
        if direction == 'right':
            xr = np.max(poly_np[:, 0])
            return xr
        if direction == 'up':
            yu = np.max(poly_np[:, 1])
            return yu
        if direction == 'down':
            yd = np.min(poly_np[:, 1])
            return yd

    def get_vias(self, via_centers):
        left = self.left + ((MERGE_WH - VIA_WH)/2)/PRECISION
        right = self.right - ((MERGE_WH - VIA_WH)/2)/PRECISION
        up = self.up - ((MERGE_WH - VIA_WH)/2)/PRECISION
        down = self.down + ((MERGE_WH - VIA_WH)/2)/PRECISION
        pos = np.where((via_centers[:, 0] > left) & (via_centers[:, 0] < right) &
        (via_centers[:, 1] > down) & (via_centers[:, 1] < up))
        self.vias = via_centers[pos]


