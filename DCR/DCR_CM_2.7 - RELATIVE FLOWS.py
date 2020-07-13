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

asset = "dcr"
asset1 = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2011-01-01"
date_2 = "2020-07-07"

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
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)
 
ax1.plot(df['date'], df['thermometer'], label='USD Price', color='aqua')
ax1.fill_between(df['date'], df['thermometer'], where=df['thermometer'] > 0, facecolor='aqua', alpha=0.4)
ax1.fill_between(df['date'], df['thermometer'], where=df['thermometer'] < 0, facecolor='red', alpha=0.7)
ax1.set_facecolor('black')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_title("Price vs Relative On-Chain Flows (142 Day)", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel('Throughput Thermometer', fontsize=20, fontweight='bold', color='w')
ax1.grid()

ax2 = ax1.twinx()
ax2.plot(df['date'], df['dcrbtc'], color='w')
""" ax2.set_yscale('log') """
ax2.tick_params(color='w', labelcolor='w')
ax2.set_ylabel(asset.upper() + 'BTC', fontsize=20, fontweight='bold', color='w')
ax2.set_yscale('log')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

plt.show()