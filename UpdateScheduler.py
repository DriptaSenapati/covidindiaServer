# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 16:14:46 2020

@author: Dripta
"""

from covidindia import *
import os
import pickle

file_path = os.path.dirname(os.path.abspath(__file__))

data_path=os.path.join(file_path,'static','server_data')


with open(os.path.join(file_path,'updater.txt'),'a') as f:
    f.write('Update Started\nGathering Data..\n')
    init = initializer(silent=True)
    with open(os.path.join(data_path, 'init.pkl'), 'wb') as init_file:
        pickle.dump(init, init_file)
    filter_data = Data(init)
    with open(os.path.join(data_path, 'filter_data.pkl'), 'wb') as filter_file:
        pickle.dump(filter_data, filter_file)
    f.write('Gathering Demographic Data...\n')
    demo = Demographic_overview(init, silent=True)
    with open(os.path.join(data_path, 'demo.pkl'), 'wb') as demo_file:
        pickle.dump(demo, demo_file)
    f.write('Gathering tested data...\n')
    tested_df = filter_data.tested_subject_data()
    tested_df.to_csv(os.path.join(data_path, 'tested_data.csv'), index=False)
    f.write('Update Done.')
    f.close()