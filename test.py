# -*- coding: utf-8 -*-
import API
import os

path = 'E:/PyCharm-wokspace/test/picture/'
api = API.API(path);
list = os.listdir(path)
for i in range(0, len(list)):
    file_path = os.path.join(path, list[i])
    if os.path.isfile(file_path) and not list[i].startswith('-'):
        api.face_detect(list[i])