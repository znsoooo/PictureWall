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


class Picture:
    def SetPicture(self, file, title):
        cv2.setWindowTitle('lsx', title)
        self.log = os.path.splitext(file)[0] + '.txt'
        img0 = cv2.imdecode(np.fromfile(file, np.uint8), -1)
        h, w, n = img0.shape
        self.k = k = min(SCREEN_WIDTH/w, SCREEN_HEIGHT/h)
        self.img = cv2.resize(img0, (int(w*k), int(h*k)))
        self.ReadLog()

    def ReadLog(self):
        self.rects = []
        if os.path.isfile(self.log):
            with open(self.log) as f:
                for rect in f.read().split('\n'):
                    self.rects.append([int(float(v) * self.k) for v in rect.split(',')])
        self.DrawRect(self.rects, (255, 0, 0))

    def SaveLog(self):
        with open(self.log, 'w') as f:
            f.write('\n'.join(','.join(str(int(v / self.k)) for v in rect) for rect in self.rects))

    def OnMouse(self, evt, x, y, flag, param):
        # print((evt, flag))
        if evt == 0 and flag == 1:
            self.OnLeftDrag(x, y)
        elif evt == 1:
            self.OnLeftDown(x, y)
        elif evt == 4:
            self.OnLeftUp(x, y)
        elif evt == 2:
            self.OnRightDown()

    def OnLeftDrag(self, x, y):
        rect = self.rects[-1] + [x, y]
        self.DrawRect([rect], (0, 255, 0))

    def OnLeftDown(self, x, y):
        self.rects.append([x, y])

    def OnLeftUp(self, x, y):
        self.rects[-1].extend([x, y])
        self.DrawRect(self.rects, (255, 0, 0))
        self.SaveLog()

    def OnRightDown(self):
        if self.rects:
            self.rects.pop()
        if not self.rects and os.path.isfile(self.log):
            os.remove(self.log)
        self.DrawRect(self.rects, (255, 0, 0))

    def DrawRect(self, rects, bgr):
        img2 = self.img.copy()
        for rect in rects:
            cv2.rectangle(img2, tuple(rect[:2]), tuple(rect[2:]), bgr, 2)
        cv2.imshow('lsx', img2)


folder = '20210122 表单统计'


pic = Picture()
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
