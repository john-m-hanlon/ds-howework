import numpy as np
import pandas as pd
from sklearn import preprocessing, svm

path = ''  # fill you path here
key_stats_csv = 'key_stats_acc_perf_NO_NA_Nov30_enhanced.csv'

t_hold = 15

FEATURES = ['DE Ratio',
            'Trailing P/E',
            'Price/Sales',
            'Price/Book',
            'Profit Margin',
            'Operating Margin',
            'Return on Assets',
            'Return on Equity',
            'Revenue Per Share',
            'Market Cap',
            'Enterprise Value',
            'Forward P/E',
            'PEG Ratio',
            'Enterprise Value/Revenue',
            'Enterprise Value/EBITDA',
            'Revenue',
            'Gross Profit',
            'EBITDA',
            'Net Income Avl to Common',
            'Diluted EPS',
            'Earnings Growth',
            'Revenue Growth',
            'Total Cash',
            'Total Cash Per Share',
            'Total Debt',
            'Current Ratio',
            'Book Value Per Share',
            'Cash Flow',
            'Beta',
            'Held by Insiders',
            'Held by Institutions',
            'Shares Short (as of',
            'Short Ratio',
            'Short % of Float',
            'Shares Short (prior ']


def Build_Data_Set():
    data_df = pd.read_csv('{}{}'.format(path, key_stats_csv))

    data_df = data_df.reindex(np.random.permutation(data_df.index))
    data_df = data_df.replace('NaN', 0).replace('N/A', 0)

    X = np.array(data_df[FEATURES].values)
    y = (data_df['status'].replace('underperform', 0).replace('outperform', 1)
                                                     .values.tolist())
    X = preprocessing.scale(X)
    # X = X.reshape(len(X), -1)

    Z = np.array(data_df[['stock p change', 'sp500 p change', 'Price',
                          'Ticker']])

    return X, y, Z


def Analysis():

    invest_amount = 100
    total_invests = 0
    if_market = 0
    if_strat = 0

    X, y, Z = Build_Data_Set()

    test_size = int(len(X) * 0.75)

    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(X[:test_size], y[:test_size])

    correct_count = 0
    ticker_list = []

    for x in range(1, test_size + 1):
        if clf.predict(X[-x])[0] == y[-x]:
            correct_count += 1

        if clf.predict(X[-x])[0] == 1:
            invest_return = invest_amount + (invest_amount * (Z[-x][0] / 100))
            market_return = invest_amount + (invest_amount * (Z[-x][1] / 100))
            if Z[-x][3] not in ticker_list:
                ticker_list.append(Z[-x][3])

            total_invests += 1
            if_market += market_return
            if_strat += invest_return

    print('Our outperformance threshold to define "status" was {}%'.
          format(t_hold))
    print('The total length of the dataset was {}'.format(len(X)))
    print('The total length of the test set was {}% or {} samples'.
          format(round((test_size / len(X) * 100), 2), test_size))
    print('We were {}% accurate with our predictions'.
          format(round((correct_count / test_size) * 100), 2))

    print('We performed {} total trades'.format(total_invests))
    print('And if we invested ${} each trade we might see the following'
          ' results...'.format(invest_amount))
    print('Ending with Strategy: {}'.format(round(if_strat), 2))
    print('Ending with Market: {}'.format(round(if_market), 2))

    compared = ((if_strat - if_market) / if_market) * 100.0
    do_nothing = total_invests * invest_amount
    print('And if we did nothing: {}'.format(do_nothing))

    avg_market = (if_market - do_nothing) / do_nothing * 100
    avg_strat = (if_strat - do_nothing) / do_nothing * 100

    print('Compared to Market, we earned: {}% more'.format(round(compared, 2)))
    print('Average Market return: {}%'.format(round(avg_market, 2)))
    print('Average Strategy return: {}%'.format(round(avg_strat, 2)))
    print('We have a list of {} unique securities to consider'.
          format(len(ticker_list)))

    print(ticker_list)
    print(len(ticker_list))


Analysis()
