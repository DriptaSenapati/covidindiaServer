# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 22:17:11 2020

@author: Dripta
"""

from covidindia import *

init=initializer()


data=Data(init)

df_3=data.get_dataset_by_date( date='25/5/2020')

df=data.get_district_data_by_date('kolkata',daily=True,date='25/5/2020')
df1=data.get_district_data_by_date('kolkata',daily=False,date='25/5/2020')
df[['active','confirmed','deceased','recovered']].cumsum(axis=0)

df=data.get_count_by_date(by='confirmed',date='22/7/2020')
