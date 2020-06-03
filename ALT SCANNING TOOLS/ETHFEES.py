import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics.
asset = "eth"
date_1 = "2011-01-01"
date_2 = "2020-06-01"

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
df['satfeeavg'] = df['satperbyte'].rolling(360).mean()
df['satfeeavg2'] = df['satperbyte'].rolling(90).mean()
df['satfeeratio'] = df['satfeeavg2'] / df['satfeeavg']

# PLOT
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('#E0E0E0')
fig.patch.set_alpha(0.7)

ax1 = plt.subplot(2, 1, 1)
plt.plot(df['date'], df['chaincost'])
plt.yscale('log')
plt.legend()
plt.grid()
plt.title("Sats per Byte")

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df['date'], df['mcap'])
plt.title("ETHUSD")
plt.yscale('log')
plt.legend()
plt.grid()
plt.show() 