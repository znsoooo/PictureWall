import os
import random

import cv2
import numpy as np


class MyList:
    def __init__(self, li):
        self.li  = li[:]
        self.li2 = []

    def pop(self):
        if not self.li2:
            self.li2 = self.li[:]
            random.shuffle(self.li2)
        return self.li2.pop()


def UniqueFile(file): # Good!
    root, ext = os.path.splitext(file)
    cnt = 1
    while os.path.exists(file):
        file = '%s_%d%s'%(root, cnt, ext)
        cnt += 1
    return file


def MyWalk(path, exts=[]):
    result = []
    for root, folders, files in os.walk(path):
        result += [os.path.join(root, file) for file in files if os.path.splitext(file)[1] in exts]
    return result


def imread(file):
    return cv2.imdecode(np.fromfile(file, np.uint8), -1)


def imwrite(file, im):
    cv2.imencode('.jpg', im)[1].tofile(file)


def imshow(img): # for test
    cv2.imshow('', img)
    cv2.waitKey(0)


def PositionIter(width, height, cols, rows, mask=None):
    if mask:
        mask = imread(mask)
        rows, cols, _ = mask.shape
    else:
        mask = np.zeros((rows, cols, 3), np.uint8)
        mask.fill(255)
    for r in range(rows):
        y1 = int(height/rows*r)
        y2 = int(height/rows*(r+1))
        for c in range(cols):
            x1 = int(width/cols*c)
            x2 = int(width/cols*(c+1))
            if mask[r][c][0]:
                yield x1, x2, y1, y2


def ConvertRect(rect=(10,20,210,120), wh=(200,100)):
    x1, y1, x2, y2 = rect          # 原方框
    x0, y0 = (x1+x2)/2, (y1+y2)/2  # 中心
    w, h = wh                      # 目标长宽比
    # 等周长变换
    L = abs(x1-x2)+abs(y1-y2)      # 周长
    w1, h1 = L*w/(w+h), L*h/(w+h)  # 新长宽
    # 返回新方框
    return (max(0,int(x0-w1/2)), max(0,int(y0-h1/2)),
            int(x0+w1/2), int(y0+h1/2))


def MakePictureWall(files, mask=None, bg_color=[255,255,255]):
    img_all = np.zeros((height, width, 3), np.uint8) # TODO 全部变色
    img_all[:,:] = bg_color
    for x1, x2, y1, y2 in PositionIter(width, height, 17, 9, mask): # 生成可分配像素位置
        w = x2 - x1
        h = y2 - y1

        log = ''
        while not os.path.isfile(log):
            file = files.pop() # 随机选取照片
            log = os.path.splitext(file)[0] + '.txt'

        img = imread(file)
        if img.shape[2] == 4: # RGBA
            if img.dtype == np.uint16: # 16位色深
                img = (img>>8).astype(np.uint8)
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        with open(log) as f:
            rect1 = [int(x) for x in f.read().split(',')]

        x1c, y1c, x2c, y2c = ConvertRect(rect1, (w,h)) # 按可分配方框调整原方框大小

        img_crop = img[y1c:y2c,x1c:x2c] # 裁切人脸
        img_crop_s = cv2.resize(img_crop, (w,h), interpolation=cv2.INTER_CUBIC) # 缩小人脸
        img_all[y1:y2,x1:x2] = img_crop_s

    if mask:
        p = '_' + os.path.splitext(os.path.basename(mask))[0]
    else:
        p = ''

    path = UniqueFile(folder+p+'.jpg')
    print('Save:', path)
    imwrite(path, img_all)



width  = 1920
height = 1080

folder = '20210122 表单统计'
files = MyList(MyWalk(folder, ['.jpg']))


##MakePictureWall(files)
##MakePictureWall(files, 'mask_666.png')
##MakePictureWall(files, 'mask_12s.png')
##MakePictureWall(files, 'mask_147.png')

##MakePictureWall(files, 'mask_0.6+.png')
MakePictureWall(files, 'mask_glink.png')
