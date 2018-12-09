# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 10:52:00 2018

@author: chael
"""

from PIL import Image

import numpy as np





img = Image.open("c:\\scratch\\world11.png")

width,height = img.size

ww = np.linspace(0,width,7)
hh =np.linspace(0,height,5)

w1 = [[[i,j]for i in ww[:-1]] for j in hh[:-1]]
w2 = [[[i,j]for i in ww[1:]] for j in hh[1:]]

length = len(w1)

for i in range(length):
    row = np.concatenate((w1[i],w2[i]),axis=1)
    ll = len(row)
    for j in range(ll):
        im = img.crop(row[j])
        im.save('c:\\scratch\\'+str(i)+str(j)+'.png')