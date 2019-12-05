import numpy as np
import pandas as pd
import os
import glob

def merge_all_csvs(path):
    all_files = glob.glob(os.path.join(path, "*.csv"))
    print(all_files)
    ## Could also use list comprehension but generator expressions are more memory friendly
    df_from_each_file = (pd.read_csv(f, names=['time_stamp', 'open', 'high_bid', 'low_bid', 'close', 'volume']) for f in all_files)
    concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
    print('Done concatinating all files, the shape is: {}'.format(concatenated_df.shape))
    ## Drop volume column as it's useless - all 0's
    concatenated_df.drop('volume', axis=1, inplace=True)
    return concatenated_df

def feature_engineering(data):
    ext = ['00', '10', '20', '30', '40', '50']
    data = data[data['time_stamp'].str.endswith(tuple(ext))]
    data['time_stamp'] = pd.to_datetime(data['time_stamp'], infer_datetime_format=True)
    data.set_index('time_stamp', inplace=True)
    data = data.astype(float)

    ## Add additional features
    data['hour'] = data.index.hour
    data['average_price'] = (data['low_bid'] + data['high_bid']) / 2.0
    data['ohlc_price'] = (data['low_bid'] + data['high_bid'] + data['open'] + data['close']) / 4.0
    data['open_close_diff'] = data['open'] - data['close']
    data['sell_or_buy'] = data['open_close_diff'].apply(lambda x: 1.0 if x > 0 else -1.0) ## 1 = BUY, -1 = SELL
    data.to_csv(r'C:\Users\945970\Desktop\random_learning_projects\FX\fx_USJPY.csv')
    csv_file = r'C:\Users\945970\Desktop\random_learning_projects\FX\fx_USJPY.csv'
    return data, csv_file
