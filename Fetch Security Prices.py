import pandas as pd
import os
import quandl
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

api_key = '-ksDg4as87XubzhJVyJQ'
path = ''
stocklist = '_KeyStats'
q = 'EOD/'
# op = 'stock_prices.csv'
op = 'stock_prices_Nov30.csv'


def stock_prices():
    ''' Searches the quandl api for adjusted close price of each security in
    our local dataset

    Parameters
    ==========

    Returns
    =======
    df : pandas dataframe
    '''
    df = pd.DataFrame()
    statspath = '{}{}'.format(path, stocklist)
    stock_list = [x[0] for x in os.walk(statspath)]
    print('Fetching stock prices...')

    for each_dir in stock_list[1:]:
        try:
            ticker = each_dir.split('/')[-1]
            query = '{}{}'.format(q, ticker)
            data = quandl.get(query, trim_start='2003-01-01',
                              trim_end='2016-11-30',
                              authtoken=api_key)
            data[ticker] = data['Adj_Close']
            df = pd.concat([df, data[ticker]], axis=1)
        except Exception as e:
            print(str(e), ticker)

    df.to_csv('{}{}'.format(path, op))
    print('Query completed...')

# stock_prices()


def plot_df():
    df = pd.read_csv('{}{}'.format(path, op))
    df.plot(x=df['Date'], legend=None)
    plt.ylim((0, 1500))
    plt.xticks(rotation=45)
    plt.show()


plot_df()
