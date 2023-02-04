# 左键框选
# 右键撤销
# 任意键盘按键切换照片
# Esc退出
# 图像自动缩放适配和框选区域等效转换记录log文本

import os
import cv2
import numpy as np


SCREEN_WIDTH  = 1900
SCREEN_HEIGHT = 900


def walk(path, exts=[]):
    result = []
    for root, folders, files in os.walk(path):
        result += [os.path.join(root, file) for file in files if os.path.splitext(file)[1] in exts]
    return result


class MyPicture:
    def SetPicture(self, file, title):
        cv2.setWindowTitle('lsx', title)
        self.log = os.path.splitext(file)[0] + '.txt'
        img0 = cv2.imdecode(np.fromfile(file, np.uint8), -1)
        h, w, n = img0.shape
        self.k = k = min(SCREEN_WIDTH/w, SCREEN_HEIGHT/h)
        self.img = cv2.resize(img0, (int(w*k), int(h*k)))
        self.ReadLog()

    def ReadLog(self):
        if os.path.isfile(self.log):
            with open(self.log) as f:
                self.rect = [int(float(x) * self.k) for x in f.read().split(',')]
        else:
            self.rect = [0, 0, 0, 0]
        self.DrawRect(self.rect, (255, 0, 0))

    def SaveLog(self):
        with open(self.log, 'w') as f:
            f.write(','.join(str(int(x / self.k)) for x in self.rect))

    def OnMouse(self, evt, x, y, flag, param):
        # print((evt, flag))
        if evt == 0 and flag == 1:
            self.OnLeftDraw(x, y)
        elif evt == 1:
            self.OnLeftDown(x, y)
        elif evt == 4:
            self.OnLeftUp(x, y)
        elif evt == 2:
            self.OnRightDown()

    def OnLeftDraw(self, x, y):
        rect_temp = self.rect[:2] + [x, y]
        self.DrawRect(rect_temp, (0, 255, 0))

    def OnLeftDown(self, x, y):
        self.rect[:2] = [x, y]

    def OnLeftUp(self, x, y):
        self.rect[2:] = [x, y]
        self.DrawRect(self.rect, (255, 0, 0))
        self.SaveLog()

    def OnRightDown(self):
        self.DrawRect((0, 0, 0, 0), (255, 0, 0))
        if os.path.isfile(self.log):
            os.remove(self.log)

    def DrawRect(self, rect, bgr):
        img2 = self.img.copy()
        cv2.rectangle(img2, tuple(rect[:2]), tuple(rect[2:]), bgr, 2)
        cv2.imshow('lsx', img2)


folder = '20210122 表单统计'


pic = MyPicture()
cv2.namedWindow('lsx')
cv2.setMouseCallback('lsx', pic.OnMouse)


paths = walk(folder, ['.jpg'])
id = 0
while True:
    path = paths[id]
    title = '(%d/%d) %s' % (id + 1, len(paths), ascii(os.path.basename(path)))
    pic.SetPicture(path, title)
    key = cv2.waitKeyEx(0)
    if key in [0x210000, 0x250000, 0x260000]:
        id = max(id - 1, 0)
    elif key in [0x220000, 0x270000, 0x280000]:
        id = min(id + 1, len(paths) - 1)
    else:
        break

cv2.destroyAllWindows()
