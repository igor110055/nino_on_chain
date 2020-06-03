# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
""" asset = "usdt" """
""" available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types) """

# List assets & dates

date_1 = "2017-01-01"
date_2 = "2020-06-01"

asset = "btc"
asset1 = "busd"
asset2 = "husd"
asset3 = "tusd"
asset4 = "usdc"
asset5 = "usdt"
asset6 = "usdt_eth"
asset7 = "usdt_trx"

#fetch desired data

btc = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2)
busd = cm.get_asset_data_for_time_range(asset1, "CapMrktCurUSD", date_1, date_2)
husd = cm.get_asset_data_for_time_range(asset2, "CapMrktCurUSD", date_1, date_2)
tusd = cm.get_asset_data_for_time_range(asset3, "CapMrktCurUSD", date_1, date_2)
usdc = cm.get_asset_data_for_time_range(asset4, "CapMrktCurUSD", date_1, date_2)
usdt = cm.get_asset_data_for_time_range(asset5, "CapMrktCurUSD", date_1, date_2)
usdt_eth = cm.get_asset_data_for_time_range(asset6, "CapMrktCurUSD", date_1, date_2)
usdt_trx = cm.get_asset_data_for_time_range(asset7, "CapMrktCurUSD", date_1, date_2)

# clean CM data for each stablecoin

btc_clean = cmdc.cm_data_convert(btc)
busd_clean = cmdc.cm_data_convert(busd)
husd_clean = cmdc.cm_data_convert(husd)
tusd_clean = cmdc.cm_data_convert(tusd)
usdc_clean = cmdc.cm_data_convert(usdc)
usdt_clean = cmdc.cm_data_convert(usdt)
usdteth_clean = cmdc.cm_data_convert(usdt_eth)
usdttrx_clean = cmdc.cm_data_convert(usdt_trx)

# clean dates

btc_dates = cmdc.cm_date_format(btc)
busd_dates = cmdc.cm_date_format(busd)
husd_dates = cmdc.cm_date_format(husd)
tusd_dates = cmdc.cm_date_format(tusd)
usdc_dates = cmdc.cm_date_format(usdc)
usdt_dates = cmdc.cm_date_format(usdt)
usdteth_dates = cmdc.cm_date_format(usdt_eth)
usdttrx_dates = cmdc.cm_date_format(usdt_trx)

# merge market caps and dates

btc_dates[''] = btc_clean
busd_dates[''] = busd_clean
husd_dates[''] = husd_clean
tusd_dates[''] = tusd_clean
usdc_dates[''] = usdc_clean
usdt_dates[''] = usdt_clean
usdteth_dates[''] = usdteth_clean
usdttrx_dates[''] = usdttrx_clean

btc_dates.columns = ['date', 'btcmarketcap']
busd_dates.columns = ['date', 'busdmarketcap']
husd_dates.columns = ['date', 'husdmarketcap']
tusd_dates.columns = ['date', 'tusdmarketcap']
usdc_dates.columns = ['date', 'usdcmarketcap']
usdt_dates.columns = ['date', 'usdtmarketcap']
usdteth_dates.columns = ['date', 'usdtethmarketcap']
usdttrx_dates.columns = ['date', 'usdttrxmarketcap']

df = btc_dates.merge(busd_dates, on='date', how='left').merge(husd_dates, on='date', how='left').merge(tusd_dates, on='date', how='left').merge(usdc_dates, on='date', how='left').merge(usdt_dates, on='date', how='left').merge(usdteth_dates, on='date', how='left').merge(usdttrx_dates, on='date', how='left')

df['Reserve Cap'] = df.sum(axis=1)
df['Reserve Ratio'] = df['btcmarketcap'] / df['Reserve Cap']
df['30 Day Avg Ratio'] = df['Reserve Ratio'].rolling(window=90).mean()
df['BTC Reserve Value'] = df['btcmarketcap'] / df['Reserve Ratio']

print(df)

#plot
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(df['date'], df['Reserve Ratio'], label='Reserve Asset Ratio')
plt.plot(df['date'], df['30 Day Avg Ratio'], label='90 Day RAR Avg')
plt.yscale('log')
plt.legend()
plt.grid()
plt.title("Reserve Asset Ratio")

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df['date'], df['btcmarketcap'], label='Bitcoin Market Cap')
plt.title("BTC Market Cap vs Reserve Value")
plt.yscale('log')
plt.legend()
plt.grid()
plt.show() 