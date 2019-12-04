from data_prep import *
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler


def create_dataset(data, lookback=20):
    data_X, data_y = [], []
    for i in range(len(data)-lookback-1):
        x = data[i:(i + lookback)]
        data_X.append(x)
        data_y.append(data[i + lookback])
    return np.array(data_X), np.array(data_y)

def explore_data(df):
    plt.figure(figsize=(15,15))
    plt.title('Pearson correlation of features', y=1.05, size=15)
    sns.heatmap(df.corr(), linewidths=0.1, vmax=1.0, square=True, linecolor='white', annot=True)
    plt.show()

    plt.figure(figsize=(15,5))
    corr = df.corr()
    sns.heatmap(corr[corr.index == 'close'], linewidths=0.1, vmax=1.0, square=True, linecolor='white', annot=True);

if __name__ == '__main__':
    path = r'C:\Users\945970\Desktop\random_learning_projects\FX\data'
    full_data = merge_all_csvs(path)
    full_data = feature_engineering(full_data)
    #explore_data(full_data)
