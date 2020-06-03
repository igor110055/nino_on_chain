import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

asset = "dcr"
asset1 = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2011-01-01"
date_2 = "2020-06-01"

dcr_flow = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "TxTfrValAdjNtv", date_1, date_2))
btc_flow = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "TxTfrValAdjNtv", date_1, date_2))

dcr_supp = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "SplyCur", date_1, date_2))
btc_supp = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "SplyCur", date_1, date_2))

dcrusd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
btcusd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "PriceUSD", date_1, date_2))

df = dcr_flow.merge(btc_flow, on='date', how='left').merge(dcr_supp, on='date', how='left').merge(btc_supp, on='date', how='left').merge(dcrusd, on='date', how='left').merge(btcusd, on='date', how='left')
df.columns = ['date', 'dcrflow', 'btcflow', 'dcrsupply', 'btcsupply', 'dcrusd', 'btcusd']

# CALC METRICS

df['dcrbtc'] = df['dcrusd'] / df['btcusd']
df['dcr142sum'] = df['dcrflow'].rolling(142).sum()
df['btc142sum'] = df['btcflow'].rolling(142).sum()
df['dcradjflow'] = df['dcr142sum'] / df['dcrsupply']
df['btcadjflow'] = df['btc142sum'] / df['btcsupply']
df['thermometer'] = (df['dcradjflow'] / df['btcadjflow']) - 1

print(df)

# PLOT

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('#E0E0E0')
fig.patch.set_alpha(0.7)
 
ax1.plot(df['date'], df['thermometer'], label='USD Price')
ax1.fill_between(df['date'], df['thermometer'], where=df['thermometer'] > 0, facecolor='green', alpha=0.25)
ax1.fill_between(df['date'], df['thermometer'], where=df['thermometer'] < 0, facecolor='red', alpha=0.25)
ax1.set_ylabel('Throughput Thermometer')
ax1.grid()

ax2 = ax1.twinx()
ax2.plot(df['date'], df['dcrbtc'], color='black', alpha=.75)
ax2.set_yscale('log')
ax2.set_ylabel('DCR / Coin Pair')

plt.title("142 Day Throughput Thermometer vs DCR / Coin")
fig.tight_layout()
plt.show()