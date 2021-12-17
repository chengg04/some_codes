import pandas as pd
import numpy as np
import csv
import util
import pdb

def read_data(all_data):
    if all_data['task'] == 'pca':
        all_data = PCA_data(all_data)
    elif all_data['task'] == 'predict' or all_data['task'] == 'plot':
        all_data = predict_data(all_data)
    elif all_data['task'] == 'normality_test':
        all_data = nrel_new_data(all_data)
    elif all_data['task'] == 'keras_bucket':
        all_data = keras_bucket_data(all_data)

    # pdb.set_trace()

    return all_data

def PCA_data(all_data):
    data_path = all_data['pwd'] + '/data/2021-2/2021-2_zoneE-Watertown.csv'
    df = pd.read_csv(data_path)
    hourly_df = df[df['Time'].str.contains(":56")]
    # pdb.set_trace()

    all_data['wind_speed'] = hourly_df['Wind Speed']
    all_data['all_wind_speed'] = {}
    all_data['all_wind_speed']['watertown'] = {}
    all_data['all_wind_speed']['watertown'][2] = df['Wind Speed']

    return all_data

def predict_data(all_data):
    zone_names = pd.read_csv(all_data['pwd'] + '/data/zone_names.csv')
    all_data['zone_names'] = zone_names['names']

    months = [2, 8]
    files = []
    for m in months: #[0:1]
        for zone in zone_names['names']:
            files.append(all_data['pwd'] + '/data/2021-' + str(m) + '/2021-' + str(m) + '_' + zone + '.csv')
    all_data['wind_df'] = pd.concat((pd.read_csv(f) for f in files), ignore_index=True) #drop=True, inplace=True keys = zone_names['names'] * len(months),

    all_data['wind_speed'] = {}
    for zone in zone_names['names']:
        all_data['wind_speed'][zone] = []
        for m in months:
            file_name = all_data['pwd'] + '/data/2021-' + str(m) + '/2021-' + str(m) + '_' + zone + '.csv'
            df = pd.read_csv(file_name)
            all_data['wind_speed'][zone] += df['Wind Speed'].tolist()

    return all_data

def nrel_new_data(all_data):
    data_path = '/Volumes/ExtraStorage/PERFORM_data/data/wind/new/wind data/'
    data_file = data_path + 'farm_speed.csv'

    all_data['nrel_new_wind_speed'] = []
    f = open(data_file, 'r')
    csvf = csv.reader(f)
    thelist = list(csvf)
    d = np.array(thelist)
    d = util.vfunc(d)
    all_data['nrel_new_wind_speed'].append(d)

    return all_data

def keras_bucket_data(all_data):
    zone_names = pd.read_csv(all_data['google_drive_path'] + '/cleaned_weather_channel_data/zone_names.csv')
    all_data['zone_names'] = zone_names['names']

    # months_str_li = ['feb', 'aug']
    # months = [2, 8]
    months_str_dict = {}
    months_str_dict[8] = 'aug'
    months = [8]
    files = []
    cnt = 0
    for zone in zone_names['names']:
        for m in months: #[0:1]
            month_str = months_str_dict[m]
            files.append(all_data['google_drive_path'] + '/cleaned_weather_channel_data/' + month_str + '2021_cleaned/cleaned_2021-' + str(m) + '_' + zone + '.csv')
    all_data['wind_df'] = pd.concat((pd.read_csv(f) for f in files), ignore_index=True) #drop=True, inplace=True keys = zone_names['names'] * len(months),

    # all_data['wind_speed'] = {}
    # for zone in zone_names['names']:
    #     all_data['wind_speed'][zone] = []
    #     for m in months:
    #         file_name = all_data['pwd'] + '/data/2021-' + str(m) + '/2021-' + str(m) + '_' + zone + '.csv'
    #         df = pd.read_csv(file_name)
    #         all_data['wind_speed'][zone] += df['Wind Speed'].tolist()

    return all_data