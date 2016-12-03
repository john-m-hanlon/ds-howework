import re
import pandas as pd
import os
import time
from datetime import datetime
import quandl
from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')


api_key = ''
path = ''
key_stats_csv = 'key_stats.csv'
stock_prices_file = 'stock_prices_Nov30.csv'
key_stats_csv_acc = 'key_stats_acc_perf_NO_NA_Nov30_enhanced.csv'

def Key_Stats(gather=['Total Debt/Equity',
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
                      'Shares Short (prior ']):

    ''' Search and full the fundamental values for each security in our list.
    This queries our data which is stored locally.

    Parameters
    ==========
    Total Debt/Equity : float
        Ratio of total liabilities to value in equity
    Trailing P/E : float
        Equal to current share price divided by earnings per share
    Price/Sales : float
        Equal to current market cap divided by annaul revenue
    Price/Book : float
        Equal to current share price divided by book value
    Profit Margin : float
        Equal to revenue less costs of goods sold expenses divided by revenue
    Operating Margin : float
        Equal to Gross Profit less selling, general, & dministration expenses
        divided by revenue
    Return on Assest : float
        Equal to annual earnings by total assets
    Return on Equity : float
        Equal to net income divided by shareholders equity
    Revenue Per Share : float
        Equal to total revenue by weighted average of shares outstanding
    Market Cap : float
        Equal to the current share price multiplied by weighted averager of
        shares outstanding
    Enterprise Value : float
        Equal to the Market Cap plus debt, non-controlling interest, preferred
        shares, less total cash and cash equivalents
    Forward P/E : float
        Equal to current share price divided by forward earnings per share
    PEG Ratio : float
        Equal to P/E divided by earnings growth rate
    Enterprise Value/Revenue : float
        Equal to Enterprise Value divided by annual revenue
    Enterprise Value/EBITDA : float
        Equal to Enterprise Value divided by EBITDA
    Revenue : float
        Equal to the total annual sales
    Gross Profit : float
        Equal to revenue less costs of goods sold expenses
    EBITDA : float
        Equal to earnings before interest, taxes, depreciation, and
        amortization
    Net Income Avl to Common : float
        Equal to net income less preferred dividends
    Diluted EPS : float
        Equal to earnings divided by diluted shares outstanding
    Earnings Growth : float
        Equal to percent change in earnings for the period
    Revenue Growth : float
        Equal to the percent change in revenue for the period
    Total Cash : float
        Equal to the total cash on hand available to the company
    Total Cash Per Share : float
        Equal to Total Cash divided by weighted average of shares outstanding
    Total Debt : float
        Equal to the summation of the company's short-term and long-term debt
    Current Ratio : float
        Equal to the current assets divided by the current liabilities
    Book Value Per Share : float
        Equal to total assets less total liabilities divied by weighted
        average shares outstanding
    Cash Flow : float
        Equal to the net amount of inflows and outflows of cash and
        cash-equivalents
    Beta : float
        Measure of volatility or systemic risk, generally provided by resource
    Held by Insiders : float
        The summation of how many shares owned, as a percentage of the
        weighted average shares outstanding, by c-level officers and directors
        of the company, or institutional investors with a least a 10% interest
        in the company
    Held by Institutions : float
        Equal to ownership, as a percentage of weighted shares outstanding, by
        large financial organizations, pension funds, or endowments
    Shares Short : float
        Equal to number of shares held short against the company
    Short Ratio : float
        Equal to Shares Short divided by weighted average of shares
        outstanding
    Short % of Float : float
        Equal to Shares Short divided by weighted average of shares
        outstanding
    Shares Short : float
        Equal to number of shares held short against the company

    Returns
    =======
    df : pandas dataframe
    '''

    print('Starting to run Key Stats...')
    stats_path = '{}_KeyStats'.format(path)
    stock_list = [x[0] for x in os.walk(stats_path)]

    df = pd.DataFrame(columns=['Date',
                               'Unix',
                               'Ticker',
                               'Price',
                               'stock p change',
                               'sp500',
                               'sp500 p change',
                               'difference',
                               'status',
                               'DE Ratio',
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
                               'Shares Short (prior '])

    sp500_df = quandl.get('EOD/SPY', authtoken=api_key)
    stock_df = pd.read_csv('{}{}'.format(path, stock_prices_file))

    ticker_list = []

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split("/")[-1]
        ticker_list.append(ticker)

        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                full_file_path = '{}/{}'.format(each_dir, file)
                source = open(full_file_path, 'r', encoding='utf8').read()
                try:
                    value_list = []
                    for each_data in gather:
                        try:
                            rx = '.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?'
                            regex = re.escape(each_data) + r'{}'.format(rx)
                            value = re.search(regex, source)
                            value = (value.group(1))

                            if 'B' in value:
                                value = float(value.
                                              replace('B', '')) * 1000000000

                            elif 'M' in value:
                                value = float(value.replace('M', '')) * 1000000

                            elif 'K' in value:
                                value = float(value.replace('K', '')) * 1000

                            value_list.append(value)

                        except:
                            value = 'N/A'
                            value_list.append(value)
# lets get the sp500 values and dates to start
                    try:
                        sp500_date = datetime.fromtimestamp(unix_time)\
                                             .strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row['Adj_Close'])
                    except:

                        try:
                            sp500_date = datetime.fromtimestamp(unix_time -
                                                                259200)\
                                                 .strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df.index == sp500_date)]
                            sp500_value = float(row['Adj_Close'])
                        except Exception as e:
                            print('ERROR IN SECTION 1: ', str(e))

                    one_year_later = int(unix_time + 31536000)
                    # one_year_later = int(unix_time + 2592000)

#  now we are getting the SP 500 values 1 year later
                    try:
                        sp500_1y = datetime.fromtimestamp(one_year_later)\
                                           .strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_1y)]
                        sp500_1y_value = float(row['Adj_Close'])
                    except Exception as e:

                        try:
                            sp500_1y = datetime.fromtimestamp(one_year_later -
                                                              259200)\
                                               .strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df.index == sp500_1y)]
                            sp500_1y_value = float(row['Adj_Close'])
                        except Exception as e:
                            print('ERROR IN SECTION 2: ', str(e))

#  getting the stock price one year later
                    try:
                        stock_price_1y = datetime.fromtimestamp(
                            one_year_later).strftime('%Y-%m-%d')
                        row = stock_df[(stock_df['Date'] ==
                                        stock_price_1y)][ticker]
                        stock_1y_value = round(float(row), 2)

                    except Exception as e:
                        try:
                            stock_price_1y = datetime.fromtimestamp(
                                one_year_later - 259200).strftime('%Y-%m-%d')
                            row = stock_df[(stock_df['Date'] ==
                                            stock_price_1y)][ticker]
                            stock_1y_value = round(float(row), 2)
                        except Exception as e:
                            print('ERROR IN SECTION 3: ', ticker, str(e))

#  now we are getting the stock price
                    try:
                        stock_price = datetime.fromtimestamp(
                            unix_time).strftime('%Y-%m-%d')
                        row = stock_df[(stock_df['Date'] ==
                                        stock_price)][ticker]
                        stock_price = round(float(row), 2)
                    except Exception as e:
                        try:
                            stock_price = datetime.fromtimestamp(
                                unix_time - 259200).strftime('%Y-%m-%d')
                            row = stock_df[(stock_df['Date'] ==
                                            stock_price)][ticker]
                            stock_price = round(float(row), 2)
                        except Exception as e:
                            print('ERROR IN SECTION 4: ', ticker, str(e))

#  define p chang
                    stock_p_change = round(((stock_1y_value - stock_price) /
                                           stock_price * 100.0), 2)

                    sp500_p_change = round(((sp500_1y_value - sp500_value) /
                                           sp500_value * 100.0), 2)

#  define the status variable and difference threshold
                    difference = stock_p_change - sp500_p_change

                    if difference > 15:
                        status = 'outperform'
                    else:
                        status = 'underperform'

                    if value_list.count('N/A') > 0:
                        pass

                    else:
                        df = df.append({'Date': date_stamp,
                                        'Unix': unix_time,
                                        'Ticker': ticker,
                                        'Price': stock_price,
                                        'stock p change': stock_p_change,
                                        'sp500': sp500_value,
                                        'sp500 p change': sp500_p_change,
                                        'difference': difference,
                                        'status': status,
                                        'DE Ratio': value_list[0],
                                        'Trailing P/E': value_list[1],
                                        'Price/Sales': value_list[2],
                                        'Price/Book': value_list[3],
                                        'Profit Margin': value_list[4],
                                        'Operating Margin': value_list[5],
                                        'Return on Assets': value_list[6],
                                        'Return on Equity': value_list[7],
                                        'Revenue Per Share': value_list[8],
                                        'Market Cap': value_list[9],
                                        'Enterprise Value': value_list[10],
                                        'Forward P/E': value_list[11],
                                        'PEG Ratio': value_list[12],
                                        'Enterprise Value/Revenue':
                                        value_list[13],
                                        'Enterprise Value/EBITDA':
                                        value_list[14],
                                        'Revenue': value_list[15],
                                        'Gross Profit': value_list[16],
                                        'EBITDA': value_list[17],
                                        'Net Income Avl to Common':
                                        value_list[18],
                                        'Diluted EPS': value_list[19],
                                        'Earnings Growth': value_list[20],
                                        'Revenue Growth': value_list[21],
                                        'Total Cash': value_list[22],
                                        'Total Cash Per Share': value_list[23],
                                        'Total Debt': value_list[24],
                                        'Current Ratio': value_list[25],
                                        'Book Value Per Share': value_list[26],
                                        'Cash Flow': value_list[27],
                                        'Beta': value_list[28],
                                        'Held by Insiders': value_list[29],
                                        'Held by Institutions': value_list[30],
                                        'Shares Short (as of': value_list[31],
                                        'Short Ratio': value_list[32],
                                        'Short % of Float': value_list[33],
                                        'Shares Short (prior ': value_list[34]
                                        }, ignore_index=True)

                except:
                    pass

    df.to_csv('{}{}'.format(path, key_stats_csv_acc))
    print('Finished running Key Stats...')


Key_Stats()

