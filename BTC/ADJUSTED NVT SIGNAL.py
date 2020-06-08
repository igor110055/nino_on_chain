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

date_1 = "2011-01-01"
date_2 = "2020-06-04"

asset = "btc"
asset1 = "busd"
asset2 = "husd"
asset3 = "tusd"
asset4 = "usdc"
asset5 = "usdt"
asset6 = "usdt_eth"
asset7 = "usdt_trx"
asset8 = "pax"

#fetch desired data

btc = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2)
btcflow = cm.get_asset_data_for_time_range(asset, "TxTfrValAdjUSD", date_1, date_2)
busd = cm.get_asset_data_for_time_range(asset1, "TxTfrValAdjUSD", date_1, date_2)
husd = cm.get_asset_data_for_time_range(asset2, "TxTfrValAdjUSD", date_1, date_2)
tusd = cm.get_asset_data_for_time_range(asset3, "TxTfrValAdjUSD", date_1, date_2)
usdc = cm.get_asset_data_for_time_range(asset4, "TxTfrValAdjUSD", date_1, date_2)
usdt = cm.get_asset_data_for_time_range(asset5, "TxTfrValAdjUSD", date_1, date_2)
usdt_eth = cm.get_asset_data_for_time_range(asset6, "TxTfrValAdjUSD", date_1, date_2)
usdt_trx = cm.get_asset_data_for_time_range(asset7, "TxTfrValAdjUSD", date_1, date_2)
pax = cm.get_asset_data_for_time_range(asset8, "TxTfrValAdjUSD", date_1, date_2)

# clean CM data for each stablecoin

btc_clean = cmdc.cm_data_convert(btc)
btcflow_clean = cmdc.cm_data_convert(btcflow)
busd_clean = cmdc.cm_data_convert(busd)
husd_clean = cmdc.cm_data_convert(husd)
tusd_clean = cmdc.cm_data_convert(tusd)
usdc_clean = cmdc.cm_data_convert(usdc)
usdt_clean = cmdc.cm_data_convert(usdt)
usdteth_clean = cmdc.cm_data_convert(usdt_eth)
usdttrx_clean = cmdc.cm_data_convert(usdt_trx)
pax_clean = cmdc.cm_data_convert(pax)

# clean dates

btc_dates = cmdc.cm_date_format(btc)
busd_dates = cmdc.cm_date_format(busd)
husd_dates = cmdc.cm_date_format(husd)
tusd_dates = cmdc.cm_date_format(tusd)
usdc_dates = cmdc.cm_date_format(usdc)
usdt_dates = cmdc.cm_date_format(usdt)
usdteth_dates = cmdc.cm_date_format(usdt_eth)
usdttrx_dates = cmdc.cm_date_format(usdt_trx)
pax_dates = cmdc.cm_date_format(pax)

# merge market caps and dates

btc_dates[''] = btc_clean
btc_dates['1'] = btcflow_clean
busd_dates[''] = busd_clean
husd_dates[''] = husd_clean
tusd_dates[''] = tusd_clean
usdc_dates[''] = usdc_clean
usdt_dates[''] = usdt_clean
usdteth_dates[''] = usdteth_clean
usdttrx_dates[''] = usdttrx_clean
pax_dates[''] = pax_clean

btc_dates.columns = ['date', 'btcmarketcap', 'btcflow']
busd_dates.columns = ['date', 'busdflow']
husd_dates.columns = ['date', 'husdflow']
tusd_dates.columns = ['date', 'tusdflow']
usdc_dates.columns = ['date', 'usdcflow']
usdt_dates.columns = ['date', 'usdtflow']
usdteth_dates.columns = ['date', 'usdtethflow']
usdttrx_dates.columns = ['date', 'usdttrxflow']
pax_dates.columns = ['date', 'paxmarketcap']

df = btc_dates.merge(busd_dates, on='date', how='left').merge(husd_dates, on='date', how='left').merge(tusd_dates, on='date', how='left').merge(usdc_dates, on='date', how='left').merge(usdt_dates, on='date', how='left').merge(usdteth_dates, on='date', how='left').merge(usdttrx_dates, on='date', how='left').merge(pax_dates, on='date', how='left')

df['Reserve Flow'] = df.iloc[:, 2:10].sum(axis=1)
df['Reserve Signal'] = df['btcmarketcap'] / df['Reserve Flow'].rolling(window=90).mean()
df['Reserve Ratio'] = df['btcmarketcap'] / df['Reserve Flow']
df['14 Day Avg Ratio'] = df['Reserve Ratio'].rolling(window=14).mean()
df['Reserve Top'] = df['Reserve Flow'].rolling(90).mean() * 75
df['Reserve Bottom'] = df['Reserve Flow'].rolling(90).mean() * 35
df['Reserve Middle'] = (df['Reserve Top'] + df['Reserve Bottom']) / 2

print(df)

#plot
plt.figure()
ax1 = plt.subplot(2, 1, 1)
""" plt.plot(df['date'], df['Reserve Ratio'], label='Reserve Asset Ratio')
plt.plot(df['date'], df['14 Day Avg Ratio'], label='14 Day RAR Avg') """
plt.plot(df['date'], df['Reserve Signal'], label='Reserve Signal', color='r')
plt.axhspan(37, 70, color='g', alpha=0.25)
plt.yscale('log')
plt.grid()
plt.legend()
plt.title("Bitcoin Market Cap / Reserve Asset Flows")

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df['date'], df['btcmarketcap'], label='BTC Market Cap')
plt.plot(df['date'], df['Reserve Top'], label='Reserve Top')
plt.plot(df['date'], df['Reserve Bottom'], label='Reserve Bottom')
plt.plot(df['date'], df['Reserve Middle'], label='Reserve Middle', linestyle=':')
plt.title("BTC Market Cap + Reserve Channels")
plt.yscale('log')
plt.legend()
plt.grid()
plt.show()