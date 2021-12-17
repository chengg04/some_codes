import requests
import json
import time
import datetime
import pandas as pd
# from pandas.io.json import json_normalize
from pandas import json_normalize # use this for newer pandas versions
import util
import pdb

def historical_data(all_data):
    api_key = "9e790c682f8b146e78ed45dd63ee7ddd"
    lat = "40.714272"
    lon = "-74.005966"
    id = "5122432"
    cnt = 200
    start_dt = datetime.date(2021,1,1)
    start_unix = int(time.mktime(start_dt.timetuple()))
    # url = "http://history.openweathermap.org/data/2.5/history/city?lat=%s&lon=%s&type=hour&start=%s&cnt=%s&appid=%s" % (
    # lat, lon, start_unix, cnt, api_key)
    url = "http://history.openweathermap.org/data/2.5/history/city?id=%s&type=hour&start=%s&cnt=%s&appid=%s" % (id, start_unix, cnt,api_key)
    # print(url)
    response = requests.get(url)
    data_json = json.loads(response.text)

    # pdb.set_trace()

    csv_file = open(all_data['pwd'] + '/data/openWeather/data_file_ithaca.csv', 'w')

    df1 = json_normalize(data_json['list'])
    df1 = df1.drop('weather', axis = 1)
    # pdb.set_trace()
    df2 = json_normalize(data_json['list'], record_path = ['weather'], record_prefix = 'weather.')
    df = df1.join(df2)
    df['main.temp'] = [util.k2f(item) for item in df['main.temp']]
    df['main.feels_like'] = [util.k2f(item) for item in df['main.feels_like']]
    df['main.temp_max'] = [util.k2f(item) for item in df['main.temp_max']]
    df['main.temp_min'] = [util.k2f(item) for item in df['main.temp_min']]

    # pdb.set_trace()

    new_col = [util.unix2time(item) for item in df['dt']]
    df.insert(loc = 0, column = 'time', value = new_col)
    # pdb.set_trace()

    df.to_csv(csv_file, index = False)



