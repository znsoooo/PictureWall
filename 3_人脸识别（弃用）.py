import os
import shutil
import random

import cv2
import numpy as np


def imread(file):
    return cv2.imdecode(np.fromfile(file, np.uint8), -1)

def imwrite(file, im):
    cv2.imencode('.jpg', im)[1].tofile(file)


def FindFaces(file, mmax, mmin=1):
    global g_file
    g_file = file
    img = imread(file)

    if file in ['20210120 表单统计2\\三部一组_赵斐_1.jpg',
                '20210120 表单统计2\\二部一组_刘鑫_1.jpg',
                '20210120 表单统计2\\管理办_王雨_1.jpg']:
        return img, 0, []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = []
    k = 1.5
    while len(faces) < mmin or len(faces) > mmax:
        try:
            faces = face_cascade.detectMultiScale(gray, k, 1, minSize=(50, 50))
        except Exception as e:
            print('Error:', '%.1f'%k, len(faces), file)

        if len(faces) < mmin:
            k -= 0.1
        else:
            k += 0.1
        if k < 0.5 or k > 3.0:
            break

    return img, k, faces


def SaveFaces(folder):
    os.makedirs(folder+'_face', exist_ok=1)
    PASS = 1
    for file in os.listdir(folder):
        if file == '管理办_王雨_1.jpg':
            PASS = 0
        if PASS:
            continue
        filename = os.path.join(folder, file)
        fileroot = os.path.join(folder+'_face', os.path.splitext(file)[0])

        img, k, faces = FindFaces(filename, mmax=3, mmin=1)
        print('%.1f'%k, len(faces), file)
        for j, (x,y,w,h) in enumerate(faces):
            img2 = img[y:y+h,x:x+w]
            imwrite('%s_%d.jpg'%(fileroot, j+1), img2)


def JoinPictures(folder, w, h, mask=None):
    files = os.listdir(folder)
    for a in range(1, max(w, h)):
        if int(w/a) * int(h/a) < len(files):
            break
    a -= 1
    gap = int(w/a) * int(h/a) - len(files)
    print('a=%d'%a)
    print('%d*%d=%d+%d'%(int(w/a), int(h/a), len(files), gap))

    files.extend(random.sample(files, gap))
    random.shuffle(files)
    img = np.zeros((int(h/a)*a, int(w/a)*a, 3))
    n = 0
    for r in range(int(h/a)):
        for c in range(int(w/a)):
            img2 = imread(os.path.join(folder, files[n]))
            img2 = cv2.resize(img2, (a, a))
            img[r*a:r*a+a, c*a:c*a+a] = img2
            n += 1
    imwrite(folder+'.jpg', img)
    return img

folder = '20210120 表单统计2'

xml = r'D:\Program Files\Python36\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(xml)

SaveFaces(folder)

##img = JoinPictures('20210120 表单统计2_face2', 1920, 1080)

