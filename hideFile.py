# -*- coding: utf-8 -*-
"""
Created on Sat May 16 10:57:48 2020

@author: Dripta
"""

import os
import ctypes
from platform import system
import json
import pandas


def hider(rootpath):
    global path
    
    if system()=='Windows':
        try:
            os.system("attrib +h " + rootpath)
            path=rootpath
        except OSError as e:
            print(e)  
            
    else:
        try:
            name="."+rootpath.split('/')[-1]
            a=rootpath.split('/')[:-1]
            a.append(name)
            newpath='/'+'/'.join(a)
            os.rename(rootpath,newpath)
            path=newpath
        except OSError as e:
            print(e) 
            
def saveFile(data,tag):
    if type(data)== pandas.core.frame.DataFrame:
        #data.to_json(path+"/"+tag+".json",orient='records')
        data.to_csv(path+"/"+tag+".csv",index=False)