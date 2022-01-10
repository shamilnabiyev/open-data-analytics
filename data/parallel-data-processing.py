from sklearn.model_selection import train_test_split
# from autogluon.tabular import TabularPredictor
from meteostat import Point, Daily
from multiprocessing import Pool
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
import time
import warnings

ALTITUDE = 10


def get_weather_data(y, m, d, lat, lon):
    # Set time period
    start = datetime(y, m, d)
    end = datetime(y, m, d)

    # Create Point for Vancouver, BC
    vancouver = Point(lat, lon, ALTITUDE)

    # Get daily data for 2018
    weather_data = Daily(vancouver, start, end)
    weather_data = weather_data.fetch()
    return weather_data


def create_weather_data(dataset):
    df_result = pd.DataFrame(
        columns=['tavg', 'tmin', 'tmax', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'df_index']
    )

    for idx, row in dataset.iterrows():
        weather_data = get_weather_data(row['year'],
                                        row['month'],
                                        row['day'],
                                        row['latitude'],
                                        row['longitude'])
        weather_data['df_index'] = idx
        df_result = pd.concat([df_result, weather_data])

    # Reset indices
    df_result = df_result.reset_index()
    df_result = df_result.rename(columns={'index': 'datetime'})
    print('df chunk %s' % dataset.index[-1], 'ready')
    return df_result


def parallelize_dataframe(dataset, func, n_cores=8):
    df_split = np.array_split(dataset, n_cores)
    pool = Pool(n_cores)
    create_weather = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return create_weather


if __name__ == '__main__':
    print('Starting parallel1 script')
    print("Start Time: %s" % time.ctime())

    df = pd.read_csv('data/df-merged.csv')
    df = df.dropna()

    weather_dat = parallelize_dataframe(df.iloc[700000:800000, :], create_weather_data)
    # print(weather_dat.head())
    print('num rows:', len(weather_dat))
    print("End Time: %s" % time.ctime())
    weather_dat.to_csv('data/weather-dat-700000-800000-v2.csv', index=False)
