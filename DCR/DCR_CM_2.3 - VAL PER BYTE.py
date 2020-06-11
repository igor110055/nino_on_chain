import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Add early price data

filename = 'DCR/DCR_data.xlsx'
df_early = pd.read_excel(filename)
early = df_early[['date', 'PriceUSD', 'PriceBTC', 'CapMrktCurUSD']].copy()
early['date'] = pd.to_datetime(early['date'], utc=True)

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# PULL DATA
asset = "dcr"
asset1 = "btc"
date1 = "2010-01-01"
date2 = "2020-06-10"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

dcrusd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date1, date2))
dcrblk = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "BlkSizeByte", date1, date2))
btcblk = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "BlkSizeByte", date1, date2))
btcusd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "PriceUSD", date1, date2))
dcrmcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date1, date2))
btcmcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "CapMrktCurUSD", date1, date2))

df = btcusd.merge(dcrblk, on='date', how='left').merge(btcblk, on='date', how='left').merge(dcrusd, on='date', how='left').merge(dcrmcap, on='date', how='left').merge(btcmcap, on='date', how='left')
df.columns = ['date', 'btcusd', 'dcrblk', 'btcblk', 'dcrusd', 'dcrmcap', 'btcmcap']

df['dcrbtc'] = df['dcrusd'] / df['btcusd']

df = df.merge(early, on='date', how='left')
df = df.fillna(0)

df['dcrusd'].mask(df['dcrusd'] == 0, df['PriceUSD'], inplace=True)
df['dcrbtc'].mask(df['dcrbtc'] == 0, df['PriceBTC'], inplace=True)
df['dcrmcap'].mask(df['dcrmcap'] == 0, df['CapMrktCurUSD'], inplace=True)

# calc metrics

df['dcrchain'] = df['dcrblk'].cumsum()
df['btcchain'] = df['btcblk'].cumsum()
df['dcrvalbyte'] = df['dcrmcap'] / df['dcrchain']
df['btcvalbyte'] = df['btcmcap'] / df['btcchain']
df['dcrbtcvalbyte'] = df['dcrvalbyte'] / df['btcvalbyte']

print(df)

# plot

name = "@permabullnino"
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
line1 = ax1.plot(df['date'], df['dcrvalbyte'], label='DCR $/Byte', color='w')
line2 = ax1.plot(df['date'], df['btcvalbyte'], label='BTC $/Byte', linestyle='dashed', color='aqua')
ax1.set_ylabel("$ / Byte", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("$ Stored per Byte Comparison", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend(edgecolor='w')

ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(df['date'], df['dcrbtcvalbyte'], color='aqua')
ax2.set_ylabel("Comparative Value Stored", fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.set_title("DCRBTC Value Stored per Byte", fontsize=20, fontweight='bold', color='w')
ax2.set_facecolor('black')
ax2.grid()

plt.show()