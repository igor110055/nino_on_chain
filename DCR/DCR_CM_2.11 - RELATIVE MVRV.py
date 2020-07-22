# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# PULL DCR & BTC NTV, MVRV, & REALIZED PRICE DATA "2016-08-14"

asset = "dcr"
asset2 = "btc"
date_1 = "2016-01-01"
date_2 = "2020-07-20"

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

df['ocratio'] = df['coin_coin1'] / df['rel_real']
df['ocratio142'] = df['ocratio'].rolling(142).mean()
df['rel_mvrv142'] = df['rel_mvrv'].rolling(142).mean()

# CALC GRADIENTS

period = 56

df['MrktGradient'] = ((df['coin_coin1'] - df['coin_coin1'].shift(periods=period, axis=0)) / period)
df['RealGradient'] = ((df['rel_real'] - df['rel_real'].shift(periods=period, axis=0)) / period)

df['DeltaGradient'] = df['MrktGradient'] - df['RealGradient']

# SEND TO EXCEL
#df.to_excel('Relative Value Prices.xlsx')

print(df)

# PLOT VALUES

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'], df['coin_coin1'], label='DCRBTC Market Traded Price', color='w')
ax1.plot(df['date'], df['rel_real'], label='DCR Realized Price / BTC Realized Price', color='lime')
ax1.plot(df['date'], df['rel_mvrv_price'], label='Relative MVRV Price', color='r')
ax1.plot(df['date'], df['mid_point'], label='Mid-Point', color='aqua')
ax1.set_ylabel("DCRBTC", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Relative Value Prices", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend()
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.plot(df['date'], df['rel_mvrv'], color='w')
ax2.plot(df['date'], df['rel_mvrv142'], color='m')
ax2.set_facecolor('black')
ax2.set_title("Relative MVRV Ratio", fontsize=20, fontweight='bold', color='w')
ax2.set_ylabel("Ratio Value", fontsize=20, fontweight='bold', color='w')
ax2.axhspan(1.05, 0.95, color='r', alpha=0.4)
ax2.axhspan(.45, 0.4, color='w', alpha=0.4)
ax2.legend()
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.grid()
for axis in [ax2.yaxis]:
    axis.set_major_formatter(ScalarFormatter())

plt.show()