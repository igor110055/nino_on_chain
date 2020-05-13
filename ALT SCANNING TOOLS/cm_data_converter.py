import coinmetrics
import matplotlib.pyplot as plt
import pandas as pd
from dateutil import parser
import datetime as dt

def cm_date_format(cm_dataset):

    sup_series = cm_dataset['series']
    sup_list = []
    sup_sup_list = []
    
    for thing in sup_series:
        sup_list.append(thing['time'])

    for item in sup_list:
        #new_item = parser.parse(item)
        new_item = pd.to_datetime(item)
        sup_sup_list.append(new_item)

    df = pd.DataFrame(sup_sup_list)

    return df

# CM Data comes in in a list-list format. This pops values out, and just puts them into a standard list

def cm_data_convert(cm_dataset):

    data_series = cm_dataset['series']
    data_list = []
    data_list_list = []
    for data in data_series:
        data_list.append(data['values'])

    for data_data in data_list:
        data_list_list.append(data_data[0])

    float_data = list(map(float, data_list_list))
    
    df_1 = pd.DataFrame(float_data)
    
    return df_1

# This calculates Market Cap / Blockchain Size for any coin you decide

def value_stored(coin, date1, date2):
    # Initialize a reference object, in this case `cm` for the Community API
    cm = coinmetrics.Community()

    # List all available metrics for coins.
    asset = coin

    available_data_types = cm.get_available_data_types_for_asset(asset)
    print("available data types:\n", available_data_types)
    #fetch desired data
    date_1 = date1
    date_2 = date2
    bchain = cm.get_asset_data_for_time_range(asset, "BlkSizeByte", date_1, date_2)
    price = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2)
    # clean CM data
    bchain_clean = cm_data_convert(bchain)
    price_clean = cm_data_convert(price)
    # convert to pandas
    df = pd.DataFrame(bchain_clean)
    df_1 = pd.DataFrame(price_clean)
    # calculate blockchain size
    size = df.cumsum()
    # calculate market cap / blockchain size
    ratio = df_1 / size
    print(ratio)
    # send to excel
    #ratio.to_excel('value_stored.xlsx')
    # plot ratio and market cap
    plt.figure()
    ax1 = plt.subplot(2, 1, 1)
    plt.plot(ratio)
    plt.yscale('log')
    plt.title("VALUE STORED / BYTE RATIO")

    plt.subplot(2, 1, 2, sharex=ax1)
    plt.plot(df_1)
    plt.title("MARKET CAP")
    plt.yscale('log')
    plt.show()

def chop_index(coin, date1, date2):
    # Initialize a reference object, in this case `cm` for the Community API
    cm = coinmetrics.Community()

    # List all available metrics for DCR.
    asset = coin

    available_data_types = cm.get_available_data_types_for_asset(asset)
    print("available data types:\n", available_data_types)
    #fetch desired data
    date_1 = date1
    date_2 = date2
    tx = cm.get_asset_data_for_time_range(asset, "TxTfrValAdjNtv", date_1, date_2)
    price = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)
    # clean CM data
    tx_clean = cm_data_convert(tx)
    price_clean = cm_data_convert(price)
    # convert to pandas
    df_2 = pd.DataFrame(tx_clean)
    df_3 = pd.DataFrame(price_clean)
    # CALC AVGS AND RATIO
    avg28 = df_2.rolling(window=28).sum()
    avg56 = df_2.rolling(window=56).sum()
    ratio = avg28 / avg56
    # plot
    plt.figure()
    ax1 = plt.subplot(2, 1, 1)
    plt.plot(ratio)
    plt.title("TX FLOWS RATIO")

    plt.subplot(2, 1, 2, sharex=ax1)
    plt.plot(df_3)
    plt.title("ALTBTC PRICE")
    plt.yscale('log')
    plt.show()

def roi_data(coin, date1, date2):
    # Initialize a reference object, in this case `cm` for the Community API
    cm = coinmetrics.Community()

    # List all available metrics.
    asset = coin

    available_data_types = cm.get_available_data_types_for_asset(asset)
    print("available data types:\n", available_data_types)

    date_1 = date1
    date_2 = date2
    roi = cm.get_asset_data_for_time_range(asset, "ROI30d", date_1, date_2)
    mcap = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2)

    roi_clean = cm_data_convert(roi)
    mcap_clean = cm_data_convert(mcap)

    df_4 = pd.DataFrame(roi_clean)
    df_5 = pd.DataFrame(mcap_clean)

    print(df_4)
    plt.figure()
    ax1 = plt.subplot(2, 1, 1)
    plt.plot(df_4)
    plt.title("30 Day ROI")

    plt.subplot(2, 1, 2, sharex=ax1)
    plt.plot(df_5)
    plt.title("Market Cap")
    plt.yscale('log')
    plt.show()