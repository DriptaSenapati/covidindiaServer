# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:38:06 2020

@author: Dripta
"""

import urllib
import json
import warnings
import pandas as pd
from datetime import datetime
import numpy as np


warnings.filterwarnings("ignore")


class districtwiseData():
    json_res = True

    def __init__(self):
        self.district_data = pd.read_csv(
            'https://api.covid19india.org/csv/latest/districts.csv')
        self.json_res = False
        self.district_dict_ = {}
        for i in np.unique(self.district_data['State']):
            self.district_dict_[i] = []
            for dis in self.district_data[self.district_data['State'] == i]['District']:
                if dis not in self.district_dict_[i]:
                    if dis != 'Unknown':
                        if dis != "Other State":
                            self.district_dict_[i].append(dis)

    def districtDate(self, district, date='All'):
        word_list = district.split(" ")
        if 'and' in word_list:
            for i, j in enumerate(word_list):
                if j != 'and':
                    word_list[i] = j.title()
            district = " ".join(word_list)
        else:
            district = district.title()
        if self.json_res == True:
            flag = 0
            if date == 'All':
                for key in self.district_data.keys():
                    for dis_name in self.district_data[key].keys():
                        if dis_name == district:
                            dis_df = pd.DataFrame(
                                self.district_data[key][dis_name]).drop(columns=['notes'])
                            flag = 1
            else:
                newdate = datetime.strftime(
                    datetime.strptime(date, '%d/%m/%Y'), '%Y-%m-%d')
                for key in self.district_data.keys():
                    for dis_name in self.district_data[key].keys():
                        if dis_name == district:
                            dis_df = pd.DataFrame(
                                self.district_data[key][dis_name]).drop(columns=['notes'])
                            dis_df = dis_df[dis_df['date'] == newdate]
                            if dis_df.empty != True:
                                flag = 1
            if flag == 1:
                return dis_df
            else:
                raise Exception(f'No data found for {district} for {date}')
        else:
            flag = 0
            if date == "All":
                dis_df = self.district_data[self.district_data['District'] == district].drop(
                    columns=['Tested','State', 'District'])
                flag = 1
            else:
                newdate = datetime.strftime(
                    datetime.strptime(date, '%d/%m/%Y'), '%Y-%m-%d')
                date_df = self.district_data[self.district_data['Date'] == newdate].drop(
                    columns=['Tested','State'])
                dis_df = date_df[date_df['District'] ==
                                 district].drop(columns=['District'])
                flag = 1

            if flag == 1:
                return dis_df.reset_index().drop(columns=['index'])
            else:
                raise Exception(f'No data found for {district} for {date}')


'''district_dict_={}
for i in np.unique(district_data_csv['State']):
    district_dict_[i]=[]
    for dis in district_data_csv[district_data_csv['State']==i]['District']:
        if dis not in district_dict_[i]:
            if dis != 'Unknown':
                if dis != "Other State":
                    district_dict_[i].append(dis)'''
