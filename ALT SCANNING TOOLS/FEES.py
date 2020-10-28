import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib.ticker as ticker

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics.
asset = "btc"
date_1 = "2010-01-01"
date_2 = "2020-10-26"

available_data_types = cm.get_available_data_types_for_asset(asset)
print(available_data_types)

Feemean = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "FeeMeanUSD", date_1, date_2))
Feemed = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "FeeMedUSD", date_1, date_2))
FeeTot = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "FeeTotUSD", date_1, date_2))
PriceUSD = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
mkt = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))
blkbytes = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "BlkSizeByte", date_1, date_2))
Feemeanntv = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "FeeMeanNtv", date_1, date_2))
Feemedntv = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "FeeMedNtv", date_1, date_2))
FeeTotntv = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "FeeTotNtv", date_1, date_2))

df = Feemean.merge(Feemed, on='date', how='left').merge(FeeTot, on='date', how='left').merge(PriceUSD, on='date', how='left').merge(mkt, on='date', how='left').merge(blkbytes, on='date', how='left').merge(Feemeanntv, on='date', how='left').merge(Feemedntv, on='date', how='left').merge(FeeTotntv, on='date', how='left')
df.columns = ['date','Feemean', 'Feemed', 'Feetot', 'PriceUSD','mcap', 'bytes', 'Feemeanntv', 'Feemedntv', 'FeeTotntv']
print(df)

# Calculate Metrics
# USD Metrics 
df['ratio'] = df['PriceUSD'] / df['Feetot']
df['feesum'] = df['Feetot'].cumsum()
df['valueratio'] = df['mcap'] / df['feesum']
df['avgcap'] = df['mcap'].rolling(90).mean()
df['blkchainsize'] = df['bytes'].cumsum()
df['chaincost'] = df['feesum'] / df['blkchainsize']

#NTV Metrics
df['feesumntv'] = df['FeeTotntv'].cumsum()
df['ntvchaincost'] = df['feesumntv'] / df['blkchainsize']
df['satperbyte'] = df['FeeTotntv'] / df['bytes']
df['satfeeavg'] = df['satperbyte'].rolling(30).mean()
df['satfeeavg2'] = df['satperbyte'].rolling(15).mean()
df['satfeeratio'] = df['satfeeavg2'] / df['satfeeavg']
df['satfeeratio2'] = df['satperbyte'] / df['satfeeavg']

# Fee Ribbon

df['ribbon_200'] = df['FeeTotntv'].rolling(window=200).mean()
df['ribbon_128'] = df['FeeTotntv'].rolling(window=128).mean()
df['ribbon_90'] = df['FeeTotntv'].rolling(window=90).mean()
df['ribbon_60'] = df['FeeTotntv'].rolling(window=60).mean()
df['ribbon_40'] = df['FeeTotntv'].rolling(window=40).mean()
df['ribbon_25'] = df['FeeTotntv'].rolling(window=25).mean()
df['ribbon_14'] = df['FeeTotntv'].rolling(window=14).mean()
df['ribbon_9'] = df['FeeTotntv'].rolling(window=9).mean()

# PLOT
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2, 1, 1)
ax1.plot(df['date'], df['FeeTotntv'], label='Fees', color='aqua', linewidth=0.5)
ax1.plot(df['date'], df['ribbon_200'], label='200', color='lime')
""" ax1.plot(df['date'], df['ribbon_128'], label='128', color='aqua', alpha=0.5)
ax1.plot(df['date'], df['ribbon_90'], label='90', color='aqua', alpha=0.5)
ax1.plot(df['date'], df['ribbon_60'], label='60', color='aqua', alpha=0.5)
ax1.plot(df['date'], df['ribbon_40'], label='40', color='aqua', alpha=0.5)
ax1.plot(df['date'], df['ribbon_25'], label='25', color='aqua', alpha=0.5)
ax1.plot(df['date'], df['ribbon_14'], label='14', color='aqua', alpha=0.5)
ax1.plot(df['date'], df['ribbon_9'], label='9', color='aqua', alpha=0.5) """
ax1.set_facecolor('black')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_title(asset.upper() + " Fees Ribbon", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel('Daily Fee Sum' + '(' + asset.upper() + ')', fontsize=20, fontweight='bold', color='w')
ax1.grid()
""" ax1.set_ylim(1, df['FeeTotntv'].max()*1.1) """
ax1.legend(loc='best')

ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.plot(df['date'], df['PriceUSD'], color='w')
ax2.set_facecolor('black')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_title(asset.upper() + "USD", fontsize=20, fontweight='bold', color='w')
ax2.set_yscale('log')
ax2.grid()
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

plt.show() 