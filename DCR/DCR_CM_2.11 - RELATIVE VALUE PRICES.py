# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# PULL DCR & BTC NTV, MVRV, & REALIZED PRICE DATA "2016-08-14"

asset = "dcr"
asset2 = "btc"
date_1 = "2016-08-14"
date_2 = "2020-06-03"

coin_price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)
coin1_price = cm.get_asset_data_for_time_range(asset2, "PriceUSD", date_1, date_2)

dcr_real = cm.get_asset_data_for_time_range(asset, "CapRealUSD", date_1, date_2)
btc_real = cm.get_asset_data_for_time_range(asset2, "CapRealUSD", date_1, date_2)

dcr_nvt = cm.get_asset_data_for_time_range(asset, "NVTAdj90", date_1, date_2)
btc_nvt = cm.get_asset_data_for_time_range(asset2, "NVTAdj90", date_1, date_2)

dcr_mvrv = cm.get_asset_data_for_time_range(asset, "CapMVRVCur", date_1, date_2)
btc_mvrv = cm.get_asset_data_for_time_range(asset2, "CapMVRVCur", date_1, date_2)

# CLEAN DATA USING DATA CONVERTER & CONVERT TO PANDAS

priceclean = cmdc.combo_convert(coin_price) #dcrprice
priceclean1 = cmdc.combo_convert(coin1_price)   #btcprice

dcrrealclean = cmdc.combo_convert(dcr_real) #dcrrealizedcap
btcrealclean = cmdc.combo_convert(btc_real)  #btcrealized cap

dcrnvtclean = cmdc.combo_convert(dcr_nvt) #dcrnvt
btcnvtclean = cmdc.combo_convert(btc_nvt)  #btcnvt

dcrmvrvclean = cmdc.combo_convert(dcr_mvrv)  #dcrmvrv
btcmvrvclean = cmdc.combo_convert(btc_mvrv)  #btcmvrv

# MERGE DATASETS
df = priceclean.merge(priceclean1, on='date', how='left').merge(dcrrealclean, on='date', how='left').merge(btcrealclean, on='date', how='left').merge(dcrnvtclean, on='date', how='left').merge(btcnvtclean, on='date', how='left').merge(dcrmvrvclean, on='date', how='left').merge(btcmvrvclean, on='date', how='left')

df.columns = ['date', 'DCRUSD', 'BTCUSD', 'DCRREAL', 'BTCREAL', 'DCRNVT', 'BTCNVT', 'DCRMVRV', 'BTCMVRV']

# CALC REALTIVE VALUE RATIOS

df['rel_real'] = df['DCRREAL'] / df['BTCREAL']
df['rel_nvt'] = df['DCRNVT'] / df['BTCNVT']
df['rel_mvrv'] = df['DCRMVRV'] / df['BTCMVRV']
df['coin_coin1'] = df['DCRUSD'] / df['BTCUSD']

# CALC RELATIVE VALUE PRICES

df['rel_nvt_price'] = df['coin_coin1'] / df['rel_nvt']
df['rel_mvrv_price'] = df['coin_coin1'] / df['rel_mvrv']
df['mid_point'] = 0.5 * (df['rel_real'] + df['rel_mvrv_price'])

# SEND TO EXCEL
#df.to_excel('Relative Value Prices.xlsx')

print(df)

# PLOT VALUES

fig = plt.figure()
fig.patch.set_facecolor('#E0E0E0')
fig.patch.set_alpha(0.7)

ax1 = plt.subplot(2,1,1)
plt.plot(df['date'], df['coin_coin1'], label='DCRBTC Market Traded Price')
plt.plot(df['date'], df['rel_real'], label='DCR Realized Price / BTC Realized Price', linestyle=':')
plt.plot(df['date'], df['rel_mvrv_price'], label='Relative MVRV Price', linestyle=':')
plt.plot(df['date'], df['mid_point'], label='Mid-Point', linestyle=':')
plt.title("Relative Value Prices")
plt.yscale('log')
plt.grid()
plt.legend()

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df['date'], df['rel_mvrv'])
plt.yscale('log')
plt.title("Relative MVRV Ratio")
plt.grid()
plt.show()