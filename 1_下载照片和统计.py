import os
import urllib.request

import xlrd

file = '20210122 表单统计.xls'


#---------------------------------------------------------------------------
# 下载照片和自动命名
#---------------------------------------------------------------------------


def urlopen(url):
    request  = urllib.request.Request(url)
    response = urllib.request.urlopen(request, timeout=5)
    return response.read()


folder = os.path.splitext(file)[0]
os.makedirs(folder, exist_ok=1)

xls = xlrd.open_workbook(file, formatting_info=True)
sheet1 = xls.sheet_by_index(0)
links = sheet1.hyperlink_map
pic_cnt = 1
names_all = set()
for r, row in enumerate(sheet1.get_rows()):
    if r == 0:
        continue

    data = [cell.value for cell in row[2:5]]
    if data[0]:
        names_all.add(data[0])
        pic_cnt    = 1
        name_last  = data[0]
        class_last = data[1]
    else:
        pic_cnt += 1
    link = links.get((r, 5)).url_or_path[:-6]

    filename = '%s_%s_%s.jpg'%(class_last, name_last, pic_cnt)

    with open(os.path.join(folder, filename), 'wb') as f:
        f.write(urlopen(link))


#---------------------------------------------------------------------------
# 筛选未交表格的名单
#---------------------------------------------------------------------------


with open('namelist.txt', encoding='u8') as f:
    s = f.read().split('\n')

cls_last = ''
for row in s:
    if not row:
        continue
    cls, name = row.split('\t')
    if cls_last != cls:
        cls_last = cls
        print('\n' + cls + '：', end='')
    
    if name and name not in names_all:
        print(name + '、', end='')

print()
print()

result = '''
二部一组：章宇尘、
二部二组：李可、
二部三组：王燕辉、刘勇、王国涛、孙红缨、朱兵、
三部一组：戚立淳、
'''

#---------------------------------------------------------------------------
# 匹配提交照片但是未匹配名单的人(错别字)
#---------------------------------------------------------------------------


for row in s:
    if not row:
        continue
    cls, name = row.split('\t')
    if name in names_all:
        names_all.remove(name)

print('Unmatch:', names_all) # Unmatch: {'付常焜'}
