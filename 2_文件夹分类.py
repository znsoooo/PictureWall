import os

join = os.path.join

folder = '20210122 表单统计'

for file in os.listdir(folder):
    if os.path.isfile(join(folder, file)):
        cls = file.split('_')[0]
        os.makedirs(join(folder, cls), exist_ok=1)
        os.rename(join(folder, file),
                  join(folder, cls, file))
