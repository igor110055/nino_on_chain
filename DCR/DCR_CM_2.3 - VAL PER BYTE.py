import coinmetrics
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

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
asset2 = "ltc"
asset3 = "eth"
date1 = "2010-01-01"
date2 = "2020-06-16"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

dcrusd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date1, date2))
dcrblk = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "BlkSizeByte", date1, date2))
btcblk = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "BlkSizeByte", date1, date2))
btcusd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "PriceUSD", date1, date2))
dcrmcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date1, date2))
btcmcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "CapMrktCurUSD", date1, date2))
dcrreal = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapRealUSD", date1, date2))
btcreal = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "CapRealUSD", date1, date2))
ltcmcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset2, "CapMrktCurUSD", date1, date2))
ltcreal = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset2, "CapRealUSD", date1, date2))
ltcblk = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset2, "BlkSizeByte", date1, date2))
ethmcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset3, "CapMrktCurUSD", date1, date2))
ethblk = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset3, "BlkSizeByte", date1, date2))

df = btcusd.merge(dcrblk, on='date', how='left').merge(btcblk, on='date', how='left').merge(dcrusd, on='date', how='left').merge(dcrmcap, on='date', how='left').merge(btcmcap, on='date', how='left').merge(dcrreal, on='date', how='left').merge(btcreal, on='date', how='left').merge(
    ltcmcap, on='date', how='left').merge(ltcreal, on='date', how='left').merge(ltcblk, on='date', how='left').merge(ethmcap, on='date', how='left').merge(ethblk, on='date', how='left')
df.columns = ['date', 'btcusd', 'dcrblk', 'btcblk', 'dcrusd', 'dcrmcap', 'btcmcap', 'dcrreal', 'btcreal', 'ltcmcap', 'ltcreal', 'ltcblk', 'ethmcap', 'ethblk']

df['dcrbtc'] = df['dcrusd'] / df['btcusd']

df = df.merge(early, on='date', how='left')
df = df.fillna(0)

df['dcrusd'].mask(df['dcrusd'] == 0, df['PriceUSD'], inplace=True)
df['dcrbtc'].mask(df['dcrbtc'] == 0, df['PriceBTC'], inplace=True)
df['dcrmcap'].mask(df['dcrmcap'] == 0, df['CapMrktCurUSD'], inplace=True)

# calc metrics

df['dcrchain'] = df['dcrblk'].cumsum()
df['btcchain'] = df['btcblk'].cumsum()
df['ltcchain'] = df['ltcblk'].cumsum()
df['ethchain'] = df['ethblk'].cumsum()
df['dcrvalbyte'] = df['dcrmcap'] / df['dcrchain']
df['btcvalbyte'] = df['btcmcap'] / df['btcchain']
df['ltcvalbyte'] = df['ltcmcap'] / df['ltcchain']
df['ethvalbyte'] = df['ethmcap'] / df['ethchain']
df['dcrbtcvalbyte'] = df['dcrvalbyte'] / df['btcvalbyte']
df['dcrrealbyte'] = df['dcrreal'] / df['dcrchain']
df['btcrealbyte'] = df['btcreal'] / df['btcchain']
df['ltcrealbyte'] = df['ltcreal'] / df['ltcchain']
df['dcrbtcrealbyte'] = df['dcrrealbyte'] / df['btcrealbyte']
df['mixedratiodcrbtc'] = df['dcrvalbyte'] / df['btcvalbyte']
df['mixedratiodcrltc'] = df['dcrvalbyte'] / df['ltcvalbyte']

df['dcrltcagg'] = df['dcrmcap'] / df['ltcmcap']
df['dcrbtcagg'] = df['dcrmcap'] / df['btcmcap']

print(df)

# plot

name = "@permabullnino"
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
line1 = ax1.plot(df['date'], df['dcrvalbyte'], label='DCR $/Byte', color='w')
line3 = ax1.plot(df['date'], df['dcrrealbyte'], label='DCR Real $/Byte', linestyle='dashed', color='r')
line2 = ax1.plot(df['date'], df['btcvalbyte'], label='BTC $/Byte', color='aqua')
line4 = ax1.plot(df['date'], df['btcrealbyte'], label='BTC Real $/Byte', linestyle='dashed', color='m')
line5 = ax1.plot(df['date'], df['ltcvalbyte'], label='LTC $/Byte', alpha=0.5)
line6 = ax1.plot(df['date'], df['ltcrealbyte'], label='LTC Real $/Byte', linestyle='dashed', alpha=0.5)
line7 = ax1.plot(df['date'], df['ethvalbyte'], label='ETH $/Byte', color='lime')
ax1.set_ylabel("$ / Byte", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("$ Stored per Byte Comparison", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.axhspan(0.95, 1.05, color='w', alpha=0.8)
ax1.grid()
ax1.legend(edgecolor='w')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

""" ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(df['date'], df['dcrbtcagg'], color='w')
ax2.plot(df['date'], df['ratio1'], color='aqua')
ax2.plot(df['date'], df['dcrbtc'], color='lime')
ax2.set_ylabel("Comparative Value Stored", fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.set_title("DCR Value Stored per Byte vs BTC & LTC", fontsize=20, fontweight='bold', color='w')
ax2.set_facecolor('black')
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
ax2.grid()
ax2.legend() """

plt.show()