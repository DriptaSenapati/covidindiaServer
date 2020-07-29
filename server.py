# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:37:28 2020

@author: Dripta
"""

from flask import Flask, jsonify, request, render_template, url_for, send_file, send_from_directory, safe_join, abort, redirect
from covidindia import *
from flask import Response
import json
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import os
from hideFile import hider, saveFile
import shutil
from platform import system
import pickle


file_path = os.path.dirname(os.path.abspath(__file__))
if system() == 'Windows':
    if os.path.exists(os.path.join(file_path, 'static', 'files')):
        shutil.rmtree(os.path.join(file_path, 'static', 'files'))
    if not os.path.exists(os.path.join(file_path, 'static', 'server_data')):
        os.mkdir(os.path.join(file_path, 'static', 'server_data'))
        print('Gathering required data....')
        init = initializer(silent=True)
        with open(os.path.join(file_path, 'static', 'server_data', 'init.pkl'), 'wb') as init_file:
            pickle.dump(init, init_file)
        filter_data = Data(init)
        with open(os.path.join(file_path, 'static', 'server_data', 'filter_data.pkl'), 'wb') as filter_file:
            pickle.dump(filter_data, filter_file)
        print('Gathering Demographic data....')
        demo = Demographic_overview(init, silent=True)
        with open(os.path.join(file_path, 'static', 'server_data', 'demo.pkl'), 'wb') as demo_file:
            pickle.dump(demo, demo_file)
        print('Gathering test data.....')
        tested_df = filter_data.tested_subject_data()
        tested_df.to_csv(os.path.join(file_path, 'static',
                                      'server_data', 'tested_data.csv'), index=False)
else:
    if os.path.exists(os.path.join(file_path, 'static', '.files')):
        shutil.rmtree(os.path.join(file_path, 'static', '.files'))
    if not os.path.exists(os.path.join(file_path, 'static', 'server_data')):
        os.mkdir(os.path.join(file_path, 'static', 'server_data'))
        print('Gathering required data....')
        init = initializer(silent=True)
        with open(os.path.join(file_path, 'static', 'server_data', 'init.pkl'), 'wb') as init_file:
            pickle.dump(init, init_file)
        filter_data = Data(init)
        with open(os.path.join(file_path, 'static', 'server_data', 'filter_data.pkl'), 'wb') as filter_file:
            pickle.dump(filter_data, filter_file)
        print('Gathering Demographic data....')
        demo = Demographic_overview(init, silent=True)
        with open(os.path.join(file_path, 'static', 'server_data', 'demo.pkl'), 'wb') as demo_file:
            pickle.dump(demo, demo_file)
        print('Gathering test data.....')
        tested_df = filter_data.tested_subject_data()
        tested_df.to_csv(os.path.join(file_path, 'static',
                                      'server_data', 'tested_data.csv'), index=False)

try:
    os.mkdir(os.path.join(file_path, 'static', 'files'))

except:
    print("Files can't be made due to some error.")

try:
    hider(os.path.join(file_path, 'static', 'files'))
except:
    print("Warning:Can't hide files")


print('Building server')
app = Flask(__name__, static_url_path='/public')
app.config["ENV"] = 'development'
app.config['SERVER_DATA'] = os.path.join(file_path, 'static', 'server_data')

if system() == 'Windows':
    app.config["CLIENT_DATA"] = os.path.join(file_path, 'static', 'files')
else:
    app.config["CLIENT_DATA"] = os.path.join(file_path, 'static', '.files')


def test_df(dataset):
    state_list = np.unique(dataset['state'])
    test_table = pd.DataFrame()
    for i in state_list:
        try:
            table = dataset[dataset['state']
                            == i].replace('', pd.NaT).dropna()
            values = table.tail(1)
            test_table = pd.concat([test_table, values])
        except:
            pass
    test_table['F'] = (test_table['positive'].astype(
        'int')/test_table['totaltested'].astype('int'))*100
    return test_table


@app.route('/', methods=['GET'])
def home():
    tested_df = pd.read_csv(os.path.join(
        file_path, 'static', 'server_data', 'tested_data.csv'))
    # with open(os.path.join(file_path, 'static', 'server_data', 'demo.pkl'), 'rb') as file:
    #demo = pickle.load(file)

    with open(os.path.join(file_path, 'static', 'server_data', 'init.pkl'), 'rb') as file:
        init = pickle.load(file)

    with open(os.path.join(file_path, 'static', 'server_data', 'filter_data.pkl'), 'rb') as file:
        filter_data = pickle.load(file)
    date = datetime.strptime(init.csv_Confirmed.columns[-1], '%m/%d/%Y')
    date = datetime.strftime(date, '%d/%m/%Y')
    conf_count = init.csv_Confirmed[init.csv_Confirmed.columns[-1]].tolist()[-1]
    change_conf = init.csv_Confirmed[init.csv_Confirmed.columns[-1]].tolist(
    )[-1]-init.csv_Confirmed[init.csv_Confirmed.columns[-2]].tolist()[-1]
    recover_count = init.csv_recovered[init.csv_recovered.columns[-1]].tolist()[-1]
    change_recover = init.csv_recovered[init.csv_recovered.columns[-1]].tolist(
    )[-1]-init.csv_recovered[init.csv_recovered.columns[-2]].tolist()[-1]
    death_count = init.csv_Death[init.csv_Death.columns[-1]].tolist()[-1]
    change_death = init.csv_Death[init.csv_Death.columns[-1]].tolist(
    )[-1]-init.csv_Death[init.csv_Death.columns[-2]].tolist()[-1]
    active_count = conf_count-recover_count-death_count
    change_active = change_conf-change_recover-change_death
    rank_df = filter_data.rank(1, 'Total Confirmed', cumulative=True)
    rank_df_rec = filter_data.rank(1, 'Total Recovered', cumulative=True)
    rank_df_death = filter_data.rank(1, 'Total Death', cumulative=True)
    f_ratio = test_df(tested_df)
    f_ratio_highest = f_ratio.sort_values(by='F', ascending=False).iloc[0, :]
    state_data = filter_data.get_dataset_state()
    state_data['recovery_rate'] = (
        state_data['Total Recovered']/state_data['Total Confirmed'])*100
    state_data['Death_rate'] = (
        state_data['Total Death']/state_data['Total Confirmed'])*100
    state_data = state_data.iloc[:-1, :].dropna()
    rec_rate_highest = state_data.sort_values(
        by='recovery_rate', ascending=False).iloc[0, :]
    death_rate_highest = state_data.sort_values(
        by='Death_rate', ascending=False).iloc[0, :]
    spike_df_conf = init.count_conf.iloc[-1, 1:]
    spike_df_rec = init.count_recover.iloc[-1, 1:]
    spike_df_death = init.count_death.iloc[-1, 1:]
    return render_template('index_dashboard.html', conf_number=conf_count, recover_number=recover_count,
                           death_number=death_count, active_number=active_count, date_1=date,
                           number_high_conf=rank_df['Total Confirmed'].values[0], state_high_conf=rank_df['STATE/UT'].values[0],
                           number_high_death=rank_df_death['Total Death'].values[
                               0], state_high_death=rank_df_death['STATE/UT'].values[0],
                           number_high_recover=rank_df_rec['Total Recovered'].values[
                               0], state_high_recover=rank_df_rec['STATE/UT'].values[0],
                           number_high_conftest=float('{0:.2f}'.format(f_ratio_highest['F'])), state_high_conftest=f_ratio_highest['state'],
                           number_high_deathrate=float('{0:.2f}'.format(death_rate_highest['Death_rate'])), state_high_deathrate=death_rate_highest['STATE/UT'],
                           number_high_recoverrate=float('{0:.2f}'.format(rec_rate_highest['recovery_rate'])), state_high_recoverrate=rec_rate_highest['STATE/UT'],
                           high_occur=max(spike_df_conf), high_occur_date=spike_df_conf[spike_df_conf == max(spike_df_conf)].index[0],
                           high_occur_rec=max(spike_df_rec), high_occur_date_rec=spike_df_rec[spike_df_rec == max(spike_df_rec)].index[0],
                           high_occur_death=max(spike_df_death), high_occur_death_date=spike_df_death[spike_df_death == max(spike_df_death)].index[0],
                           up_text_conf=change_conf, up_text_active=change_active, up_text_recover=change_recover,
                           up_text_death=change_death)


@app.route('/data', methods=['GET', 'POST'])
def data():
    with open(os.path.join(file_path, 'static', 'server_data', 'init.pkl'), 'rb') as file:
        init = pickle.load(file)
    if request.method == 'GET':
        '''for i in ['Confirmed','Recovered','Death']:
            df = init.show_data(of=i)
            saveFile(df, i)'''
        return render_template('index_home.html')
    elif request.method == 'POST':
        value = request.form['result_data']
        daily = request.form['daily_data']
        if daily == 'No':
            df = init.show_data(of=value.split(' ')[1])
            saveFile(df, f'{value}-{daily}')
            df = df.to_json(orient='records')
        else:
            df = init.show_data(of=value.split(' ')[1], daily=True)
            saveFile(df, f'{value}-{daily}')
            df = df.to_json(orient='records')

        return df


@app.route('/State', methods=['GET', 'POST'])
def state():
    with open(os.path.join(file_path, 'static', 'server_data', 'filter_data.pkl'), 'rb') as file:
        filter_data = pickle.load(file)
    if request.method == 'GET':
        return render_template('index_state.html')
    elif request.method == 'POST':
        state_name = request.form['state_data']
        district_name = request.form['district_data']
        date_name = request.form['date_data']
        daily = request.form['daily_data']
        if state_name == 'All':
            if date_name == 'All':
                if daily == 'Yes':
                    df = filter_data.get_dataset_state(
                        state='Whole', daily=True)
                    saveFile(
                        df, f'{state_name}-{district_name}-{date_name}-{daily}')
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                else:
                    df = filter_data.get_dataset_state(
                        state='Whole', daily=False)
                    saveFile(
                        df, f'{state_name}-{district_name}-{date_name}-{daily}')
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
            else:
                df_confirmed = filter_data.get_count_by_date(
                    by='confirmed', date=date_name)
                df_recovered = filter_data.get_count_by_date(
                    by='recovered', date=date_name)
                df_death = filter_data.get_count_by_date(
                    by='death', date=date_name)
                df = pd.merge(df_confirmed, df_recovered, on='STATE/UT')
                df = pd.merge(df, df_death, on='STATE/UT')
                df.columns = ['STATE/UT', 'Confirmed', 'Recovered', 'Death']
                saveFile(
                    df, f'{state_name}-{district_name}-({date_name.replace("/","-")})-{daily}')
                df = df.to_json(orient='records')
                return Response(df,  mimetype='application/json')

        else:
            if district_name == 'All':
                if date_name == 'All':
                    if daily == 'Yes':
                        df = filter_data.get_dataset_state(
                            state=state_name, daily=True).reset_index()
                        df.columns = ['Date', 'Confirmed',
                                      'Recovered', 'Death']
                        saveFile(
                            df, f'{state_name}-{district_name}-{date_name}-{daily}')
                        df = df.to_json(orient='records')

                        return Response(df,  mimetype='application/json')
                    else:
                        df = filter_data.get_dataset_state(
                            state=state_name, daily=False)
                        saveFile(
                            df, f'{state_name}-{district_name}-{date_name}-{daily}')
                        df = df.to_json(orient='records')
                        return Response(df,  mimetype='application/json')
                else:
                    if daily == 'No':
                        df = filter_data.get_district_data_by_date(
                            state_name, date=date_name)
                        saveFile(
                            df, f'{state_name}-{district_name}-({date_name.replace("/","-")})-{daily}')
                        df = df.to_json(orient='records')
                        return Response(df,  mimetype='application/json')
                    else:
                        df = filter_data.get_district_data_by_date(
                            state_name, date=date_name, daily=True)
                        saveFile(
                            df, f'{state_name}-{district_name}-({date_name.replace("/","-")})-{daily}')
                        df = df.to_json(orient='records')
                        return Response(df,  mimetype='application/json')
            else:
                if date_name == 'All':
                    if daily == 'Yes':
                        df = filter_data.get_district_data_by_date(
                            district_name, daily=True)
                        saveFile(
                            df, f'{state_name}-{district_name}-{date_name}-{daily}')
                        df = df.to_json(orient='records')
                        return Response(df,  mimetype='application/json')
                    else:
                        df = filter_data.get_district_data_by_date(
                            district_name, daily=False)
                        saveFile(
                            df, f'{state_name}-{district_name}-{date_name}-{daily}')
                        df = df.to_json(orient='records')
                        return Response(df,  mimetype='application/json')
                else:
                    if daily == 'Yes':
                        df = filter_data.get_district_data_by_date(
                            district_name, date=date_name, daily=True)
                        saveFile(
                            df, f'{state_name}-{district_name}-({date_name.replace("/","-")})-{daily}')
                        df = df.to_json(orient='records')
                        return Response(df,  mimetype='application/json')
                    else:
                        df = filter_data.get_district_data_by_date(
                            district_name, date=date_name)
                        saveFile(
                            df, f'{state_name}-{district_name}-({date_name.replace("/","-")})-{daily}')
                        df = df.to_json(orient='records')
                        return Response(df,  mimetype='application/json')


@app.route('/Demography', methods=['GET', 'POST'])
def demography():
    with open(os.path.join(file_path, 'static', 'server_data', 'demo.pkl'), 'rb') as file:
        demo = pickle.load(file)
    if request.method == 'GET':
        return render_template('index_demo.html')
    elif request.method == 'POST':
        place = request.form['place_data']
        date = request.form['date_day']
        try:
            df = demo.demography(place=place.lower(),
                                 date=date.lower()).reset_index()
            for i, j in enumerate(df.dateannounced):
                df.dateannounced[i] = datetime.strftime(j, '%d/%m/%Y')
            if date != 'All':
                tag = date.replace('/', '-')
                saveFile(df, f'{place}-({tag})')
            else:
                saveFile(df, f'{place}-{date}')
            df = df.to_json(orient='records')
            return Response(df,  mimetype='application/json')
        except:
            return 'None'


@app.route('/filter', methods=['POST'])
def disfilter():
    with open(os.path.join(file_path, 'static', 'server_data', 'demo.pkl'), 'rb') as file:
        demo = pickle.load(file)
    place_name = request.form['place_data']
    df = demo.raw[demo.raw['detectedstate'] == place_name]
    if df.empty == False:
        result_list = list(
            np.unique([i for i in df['detecteddistrict']]))
        return Response(json.dumps(result_list),  mimetype='application/json')
    else:
        df = demo.raw[demo.raw['detecteddistrict'] == place_name]
        result_list = list(np.unique([i for i in df['detectedcity']]))
        return Response(json.dumps(result_list),  mimetype='application/json')


@app.route('/Rank', methods=['GET', 'POST'])
def rank():
    with open(os.path.join(file_path, 'static', 'server_data', 'filter_data.pkl'), 'rb') as file:
        filter_data = pickle.load(file)
    if request.method == 'GET':
        return render_template('index_rank.html')
    elif request.method == 'POST':
        kind = request.form['kind_data']
        num = int(request.form['number_data'])
        by = request.form['by_data']
        cumulative = request.form['cumulative_data']
        date = request.form['date_data']
        if date == 'None':
            if cumulative == 'False':
                state = request.form['state_data']
                df = filter_data.rank(
                    num=num, by=by, kind=kind.lower(), cumulative=False)
                df = pd.DataFrame(df[state]).reset_index()
                df.columns = ['Date', f'{state}']
                saveFile(df, f'{kind}-{num}-{by}-Daily-AllDate-{state}')
                df = df.to_json(orient='records')
                return Response(df,  mimetype='application/json')
            else:
                df = filter_data.rank(
                    num=num, by=by, kind=kind.lower(), cumulative=True)
                saveFile(df, f'{kind}-{num}-{by}-Cumulative-AllDate')
                df = df.to_json(orient='records')
                return Response(df,  mimetype='application/json')

        else:
            if cumulative == 'False':
                df = filter_data.rank(
                    num=num, by=by, kind=kind.lower(), cumulative=False, date=date)
                saveFile(
                    df, f'{kind}-{num}-{by}-Daily-({date.replace("/","-")})')
                df = df.to_json(orient='records')
                return Response(df,  mimetype='application/json')
            else:
                df = filter_data.rank(
                    num=num, by=by, kind=kind.lower(), cumulative=True, date=date)
                saveFile(
                    df, f'{kind}-{num}-{by}-Cumulative-({date.replace("/","-")})')
                df = df.to_json(orient='records')
                return Response(df,  mimetype='application/json')


@app.route('/analysis', methods=['GET'])
def analysis():
    global init, demo, filter_data, tested_df
    tested_df = pd.read_csv(os.path.join(
        file_path, 'static', 'server_data', 'tested_data.csv'))
    with open(os.path.join(file_path, 'static', 'server_data', 'demo.pkl'), 'rb') as file:
        demo = pickle.load(file)

    with open(os.path.join(file_path, 'static', 'server_data', 'init.pkl'), 'rb') as file:
        init = pickle.load(file)

    with open(os.path.join(file_path, 'static', 'server_data', 'filter_data.pkl'), 'rb') as file:
        filter_data = pickle.load(file)
    if request.method == 'GET':
        return render_template('index_analysis.html')


@app.route('/tested', methods=['POST'])
def tested():
    global init, demo, filter_data, tested_df
    ratio = request.form['ratio_data']
    state_list = init.csv_Confirmed['STATE/UT']
    test_table = pd.DataFrame()
    for i in state_list:
        try:
            table = tested_df[tested_df['state']
                              == i].replace('', pd.NaT).dropna()
            values = table.tail(1)
            test_table = pd.concat([test_table, values])
        except:
            pass
    test_table['F'] = (test_table['positive'].astype(
        'int')/test_table['totaltested'].astype('int'))*100
    tested_population = [init.csv_Confirmed[init.csv_Confirmed['STATE/UT']
                                            == i]['POPULATION'].values[0] for i in test_table['state']]
    tested_population = [int(i.replace(',', ''))
                         for i in tested_population]
    test_table['Population'] = tested_population
    if ratio == 'true':
        dataset = test_table.sort_values(by='F', ascending=False)
        dataset = dataset.to_json(orient='records')
        return Response(dataset,  mimetype='application/json')
    else:
        test_table['totaltested'] = test_table['totaltested'].astype(
            'int')
        test_table['test_pop_ratio'] = (
            test_table['totaltested']/test_table['Population'])*10000
        dataset = test_table.sort_values(
            by='test_pop_ratio', ascending=False)
        dataset = dataset.to_json(orient='records')
        return Response(dataset,  mimetype='application/json')


@app.route('/date/<endpoint>', methods=['GET', 'POST'])
def date(endpoint):
    with open(os.path.join(file_path, 'static', 'server_data', 'init.pkl'), 'rb') as file:
        init = pickle.load(file)
    if endpoint == 'rank' or endpoint == 'demo':
        if request.method == 'GET':
            csv = init.csv_Confirmed
            lastDate = csv.columns[-1]
            return lastDate
    elif endpoint == 'state':
        if request.method == 'POST':
            state_data = request.form['state']
            df = init.district_data.district_data
            state_df = df[df['State'] == state_data]
            startdate = list(state_df.sort_values('Date')['Date'])[0]
            enddate = datetime.strftime(datetime.strptime(list(state_df.sort_values('Date')[
                                        'Date'])[-1], '%Y-%m-%d')-timedelta(1), '%Y-%m-%d')
            # enddate=list(state_df.sort_values('Date')['Date'])[-1]
            returnlist = [startdate, enddate]
            return Response(json.dumps(returnlist),  mimetype='application/json')


@app.route('/rec_dec_rate', methods=['POST'])
def rate():
    with open(os.path.join(file_path, 'static', 'server_data', 'filter_data.pkl'), 'rb') as file:
        filter_data = pickle.load(file)
    rate_data = request.form['rate']
    state_data = filter_data.get_dataset_state()
    state_data['recovery_rate'] = (
        state_data['Total Recovered']/state_data['Total Confirmed'])*100
    state_data['Death_rate'] = (
        state_data['Total Death']/state_data['Total Confirmed'])*100
    state_data = state_data.iloc[:-1, :].dropna()
    if rate_data == 'recovered':
        dataset = state_data.sort_values(
            by='recovery_rate', ascending=False)
        dataset = dataset.to_json(orient='records')
        return Response(dataset,  mimetype='application/json')
    elif rate_data == 'deceased':
        dataset = state_data.sort_values(
            by='Death_rate', ascending=False)
        dataset = dataset.to_json(orient='records')
        return Response(dataset,  mimetype='application/json')


@app.route('/statistics/<gtype>', methods=['GET', 'POST'])
def graphtype(gtype):
    global init, demo, filter_data
    if gtype == 'age_bar_chart':
        age_data = demo.raw[demo.raw['agebracket'] != 'Unknown'].reset_index()
        age_data = age_data.drop(columns=['index']).tail(1000)
        age_series = list(age_data['agebracket'])
        print(len(age_series))
        for i, j in enumerate(age_series):
            if '-' in j:
                l = j.split('-')
                age_series[i] = (float(l[0])+float(l[1]))/2
            else:
                try:
                    age_series[i] = float(j)
                except:
                    age_series[i] = float(j.split(' ')[0])
        age_bar_dict = {'age': [], 'count': []}
        for i in np.arange(0, max(age_series) + 1, 10):
            temp_list = []
            age_bar_dict['age'].append(f'({i},{i+10})')
            for j in age_series:
                if j >= i:
                    if j < i+10:
                        temp_list.append(j)
            age_bar_dict['count'].append(
                len(temp_list))
        age_bar = pd.DataFrame(age_bar_dict)
        age_bar = age_bar.to_json(orient='records')
        return Response(age_bar,  mimetype='application/json')
    elif gtype == 'rolling_growth':
        if request.method == 'POST':
            rolling_value = int(request.form['rolling'])
            state_data = init.count_conf
            state_data = state_data[state_data['STATE/UT']
                                    != "Unassigned State"]
            state_rolling_data = state_data.iloc[:-1,
                                                 1:].rolling(rolling_value, axis=1).mean()
            state_rolling_data = pd.concat(
                [state_data['STATE/UT'][:-1], state_rolling_data], axis=1)
            state_rolling_data = state_rolling_data.fillna(0)
            state_rolling_data = state_rolling_data.to_json(orient='records')
            return Response(state_rolling_data,  mimetype='application/json')
    elif gtype == 'corona_graph':
        if request.method == 'POST':
            state_name = request.form['state_data'].replace('"', '')
            daily = request.form['daily_data'].replace('"', '')
            condition = request.form['condition_data'].replace('"', '')
            last = int(request.form['silder_data'])
            if last == 0:
                if state_name == 'All':
                    if daily == 'Yes':
                        if condition == 'Confirmed':
                            df = init.count_conf
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Recovered':
                            df = init.count_recover
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Deceased':
                            df = init.count_death
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Together':
                            df_1 = init.count_conf.to_json(
                                orient='records')
                            df_2 = init.count_recover.to_json(
                                orient='records')
                            df_3 = init.count_death.to_json(
                                orient='records')
                            df_list = [df_1, df_2, df_3]
                            return Response(json.dumps(df_list),  mimetype='application/json')
                    else:
                        if condition == 'Confirmed':
                            df = init.csv_Confirmed
                            df = df.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR)', 'LONGITUDE',
                                                  'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Recovered':
                            df = init.csv_recovered
                            df = df.drop(columns=['POPULATION', 'LONGITUDE', 'PER CAPITA INCOME (INR)',
                                                  'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Deceased':
                            df = init.csv_Death
                            df = df.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR) ', 'LONGITUDE',
                                                  'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Together':
                            df_1 = init.csv_Confirmed.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR)', 'LONGITUDE',
                                                                    'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                            df_1 = df_1.to_json(orient='records')
                            df_2 = init.csv_recovered.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR)', 'LONGITUDE',
                                                                    'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                            df_2 = df_2.to_json(orient='records')
                            df_3 = init.csv_Death.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR) ', 'LONGITUDE',
                                                                'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                            df_3 = df_3.to_json(orient='records')
                            df_list = [df_1, df_2, df_3]
                            return Response(json.dumps(df_list),  mimetype='application/json')
                else:
                    if daily == 'Yes':
                        if condition == 'Confirmed':
                            df = init.count_conf[init.count_conf['STATE/UT']
                                                 == state_name]
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Recovered':
                            df = init.count_recover[init.count_recover['STATE/UT']
                                                    == state_name]
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Deceased':
                            df = init.count_death[init.count_death['STATE/UT']
                                                  == state_name]
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Together':
                            df_1 = init.count_conf[init.count_conf['STATE/UT']
                                                   == state_name].to_json(orient='records')
                            df_2 = init.count_recover[init.count_recover['STATE/UT']
                                                      == state_name].to_json(orient='records')
                            df_3 = init.count_death[init.count_death['STATE/UT']
                                                    == state_name].to_json(orient='records')
                            df_list = [df_1, df_2, df_3]
                            return Response(json.dumps(df_list),  mimetype='application/json')
                    else:
                        if condition == 'Confirmed':
                            df = init.csv_Confirmed[init.csv_Confirmed['STATE/UT']
                                                    == state_name]
                            df = df.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR)', 'LONGITUDE',
                                                  'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Recovered':
                            df = init.csv_recovered[init.csv_recovered['STATE/UT']
                                                    == state_name]
                            df = df.drop(columns=['POPULATION', 'LONGITUDE', 'PER CAPITA INCOME (INR)',
                                                  'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Deceased':
                            df = init.csv_Death[init.csv_Death['STATE/UT']
                                                == state_name]
                            df = df.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR) ', 'LONGITUDE',
                                                  'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Together':
                            df_1 = init.csv_Confirmed[init.csv_Confirmed['STATE/UT'] == state_name].drop(columns=['POPULATION', 'PER CAPITA INCOME (INR)', 'LONGITUDE',
                                                                                                                  'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                            df_1 = df_1.to_json(orient='records')
                            df_2 = init.csv_recovered[init.csv_recovered['STATE/UT'] == state_name].drop(columns=['POPULATION', 'PER CAPITA INCOME (INR)', 'LONGITUDE',
                                                                                                                  'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                            df_2 = df_2.to_json(orient='records')
                            df_3 = init.csv_Death[init.csv_Death['STATE/UT'] == state_name].drop(columns=['POPULATION', 'PER CAPITA INCOME (INR) ', 'LONGITUDE',
                                                                                                          'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                            df_3 = df_3.to_json(orient='records')
                            df_list = [df_1, df_2, df_3]
                            return Response(json.dumps(df_list),  mimetype='application/json')
            else:
                endDate = datetime.strptime(
                    init.csv_Confirmed.columns[-1], '%m/%d/%Y')
                lastdate = datetime.strftime(endDate, '%d/%m/%Y')
                startDate = datetime.strftime(
                    endDate-timedelta(last), '%d/%m/%Y')
                if state_name == 'All':
                    if daily == 'Yes':
                        if condition == 'Confirmed':
                            df = filter_data.get_count_between_date(
                                startDate, lastdate, condition)
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Recovered':
                            df = filter_data.get_count_between_date(
                                startDate, lastdate, condition)
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Deceased':
                            df = filter_data.get_count_between_date(
                                startDate, lastdate, 'Death')
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Together':
                            df_1 = filter_data.get_count_between_date(
                                startDate, lastdate, 'Confirmed').to_json(orient='records')
                            df_2 = filter_data.get_count_between_date(
                                startDate, lastdate, 'Recovered').to_json(orient='records')
                            df_3 = filter_data.get_count_between_date(
                                startDate, lastdate, 'Death').to_json(orient='records')
                            df_list = [df_1, df_2, df_3]
                            return Response(json.dumps(df_list),  mimetype='application/json')
                    else:
                        if condition == 'Confirmed':
                            df = filter_data.get_cum_dataset_between_date(
                                startDate, lastdate, 'Total Confirmed')
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Recovered':
                            df = filter_data.get_cum_dataset_between_date(
                                startDate, lastdate, 'Total Recovered')
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Deceased':
                            df = filter_data.get_cum_dataset_between_date(
                                startDate, lastdate, 'Total Death')
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Together':
                            df_1 = filter_data.get_cum_dataset_between_date(
                                startDate, lastdate, 'Total Confirmed').to_json(orient='records')
                            df_2 = filter_data.get_cum_dataset_between_date(
                                startDate, lastdate, 'Total Recovered').to_json(orient='records')
                            df_3 = filter_data.get_cum_dataset_between_date(
                                startDate, lastdate, 'Total Death').to_json(orient='records')
                            df_list = [df_1, df_2, df_3]
                            return Response(json.dumps(df_list),  mimetype='application/json')
                else:
                    if daily == 'Yes':
                        if condition == 'Confirmed':
                            df = filter_data.get_count_between_date(
                                startDate, lastdate, condition)
                            df = df[df['STATE/UT']
                                    == state_name]
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Recovered':
                            df = filter_data.get_count_between_date(
                                startDate, lastdate, condition)
                            df = df[df['STATE/UT']
                                    == state_name]
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Deceased':
                            df = filter_data.get_count_between_date(
                                startDate, lastdate, 'Death')
                            df = df[df['STATE/UT']
                                    == state_name]
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Together':
                            df_1 = filter_data.get_count_between_date(
                                startDate, lastdate, 'Confirmed')
                            df_1 = df_1[df_1['STATE/UT']
                                        == state_name].to_json(orient='records')
                            df_2 = filter_data.get_count_between_date(
                                startDate, lastdate, 'Recovered')
                            df_2 = df_2[df_2['STATE/UT']
                                        == state_name].to_json(orient='records')
                            df_3 = filter_data.get_count_between_date(
                                startDate, lastdate, 'Death')
                            df_3 = df_3[df_3['STATE/UT']
                                        == state_name].to_json(orient='records')
                            df_list = [df_1, df_2, df_3]
                            return Response(json.dumps(df_list),  mimetype='application/json')
                    else:
                        if condition == 'Confirmed':
                            df = filter_data.get_cum_dataset_between_date(
                                startDate, lastdate, 'Total Confirmed')
                            df = df[df['STATE/UT']
                                    == state_name]
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Recovered':
                            df = filter_data.get_cum_dataset_between_date(
                                startDate, lastdate, 'Total Recovered')
                            df = df[df['STATE/UT']
                                    == state_name]
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Deceased':
                            df = filter_data.get_cum_dataset_between_date(
                                startDate, lastdate, 'Total Death')
                            df = df[df['STATE/UT']
                                    == state_name]
                            df = df.to_json(orient='records')
                            return Response(df,  mimetype='application/json')
                        elif condition == 'Together':
                            df_1 = filter_data.get_cum_dataset_between_date(
                                startDate, lastdate, 'Total Confirmed')
                            df_1 = df_1[df_1['STATE/UT'] == state_name]
                            df_1 = df_1.to_json(orient='records')
                            df_2 = filter_data.get_cum_dataset_between_date(
                                startDate, lastdate, 'Total Recovered')
                            df_2 = df_2[df_2['STATE/UT'] == state_name]
                            df_2 = df_2.to_json(orient='records')
                            df_3 = filter_data.get_cum_dataset_between_date(
                                startDate, lastdate, 'Total Death')
                            df_3 = df_3[df_3['STATE/UT'] == state_name]
                            df_3 = df_3.to_json(orient='records')
                            df_list = [df_1, df_2, df_3]
                            return Response(json.dumps(df_list),  mimetype='application/json')

    elif gtype == 'mapdata':
        if request.method == 'POST':
            with open(os.path.join(file_path, 'static', 'server_data', 'init.pkl'), 'rb') as file:
                init = pickle.load(file)
            reject_list = ['la', 'ld', 'tg', 'ut', 'un', 'tt']
            dtype = request.form['dtype']
            if dtype == 'confirmed':
                conf = init.show_data(of='confirmed', daily=False)
                df = conf[['CODE', f'{conf.columns[-1]}']]
                df = pd.concat([df, pd.DataFrame({'CODE': [
                               'IN-UT'], f'{conf.columns[-1]}':[0]})]).reset_index().drop(columns=['index'])
            elif dtype == 'recovered':
                recover = init.show_data(of='recovered', daily=False)
                df = recover[['CODE', f'{recover.columns[-1]}']]
                df = pd.concat([df, pd.DataFrame({'CODE': [
                               'IN-UT'], f'{recover.columns[-1]}':[0]})]).reset_index().drop(columns=['index'])
            elif dtype == 'death':
                death = init.show_data(of='death', daily=False)
                df = death[['CODE', f'{death.columns[-1]}']]
                df = pd.concat([df, pd.DataFrame({'CODE': [
                               'IN-UT'], f'{death.columns[-1]}':[0]})]).reset_index().drop(columns=['index'])
            elif dtype == 'active':
                conf = init.show_data(of='confirmed', daily=False)
                recover = init.show_data(of='recovered', daily=False)
                death = init.show_data(of='death', daily=False)
                active_series = conf[f'{conf.columns[-1]}'] - \
                    recover[f'{recover.columns[-1]}'] - \
                    death[f'{death.columns[-1]}']
                df = pd.concat([pd.DataFrame(conf['CODE']),
                                pd.DataFrame(active_series)], axis=1)
            for i in df.index:
                if df.loc[i, 'CODE'] not in reject_list:
                    df.loc[i, 'CODE'] = 'IN-'+df.loc[i, 'CODE'].upper()
                else:
                    df.drop([i], inplace=True)

            resp = {}
            for i in df.index:
                resp[df.loc[i, 'CODE']] = df.loc[i, f'{df.columns[-1]}']
            print(resp)
            g = pd.DataFrame([resp])
        return Response(g.to_json(orient='records'),  mimetype='application/json')


@app.route('/get-json/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    try:
        filename = f'{filename}.json'
        return send_from_directory(app.config["CLIENT_DATA"], filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
    # return send_file(path, as_attachment=True)


@app.route('/get-csv/<path:filename>', methods=['GET', 'POST'])
def download_file_csv(filename):
    try:
        filename = f'{filename}.csv'
        return send_from_directory(app.config["CLIENT_DATA"], filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/refresh/<endpoint>', methods=['GET'])
def refresh(endpoint):
    global init, demo, filter_data
    init_refresh = initializer(silent=True)
    if init_refresh.csv_Confirmed.columns[-1] != init.csv_Confirmed.columns[-1]:
        print('Updating required Data.....', end='\r')
        with open(os.path.join(file_path, 'static', 'server_data', 'init.pkl'), 'wb') as init_file:
            pickle.dump(init_refresh, init_file)
        filter_data = Data(init_refresh)
        with open(os.path.join(file_path, 'static', 'server_data', 'filter_data.pkl'), 'wb') as filter_file:
            pickle.dump(filter_data, filter_file)
        print('Updating demographic data....', end='\r')
        demo = Demographic_overview(init_refresh, silent=True)
        with open(os.path.join(file_path, 'static', 'server_data', 'demo.pkl'), 'wb') as demo_file:
            pickle.dump(demo, demo_file)
        print('Updating tested data', end='\r')
        tested_df = filter_data.tested_subject_data()
        tested_df.to_csv(os.path.join(file_path, 'static',
                                      'server_data', 'tested_data.csv'), index=False)
        tested_df = pd.read_csv(os.path.join(
            file_path, 'static', 'server_data', 'tested_data.csv'))

        with open(os.path.join(file_path, 'static', 'server_data', 'demo.pkl'), 'rb') as file:
            demo = pickle.load(file)

        with open(os.path.join(file_path, 'static', 'server_data', 'init.pkl'), 'rb') as file:
            init = pickle.load(file)

        with open(os.path.join(file_path, 'static', 'server_data', 'filter_data.pkl'), 'rb') as file:
            filter_data = pickle.load(file)

        return redirect(url_for(f'{endpoint}'))
    else:
        return 'Updated'


if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=True)
