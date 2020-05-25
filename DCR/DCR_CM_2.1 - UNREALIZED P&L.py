# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List the assets Coin Metrics has data for.
supported_assets = cm.get_supported_assets()
print("supported assets:\n", supported_assets)

# List all available metrics for DCR.
asset = "dcr"
date1 = "2016-02-08"
date2 = "2020-05-21"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

# retrieve the historical data for realized cap / market cap & merge cata

real_cap = cm.get_real_cap(asset, date1, date2)
mcap = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date1, date2)
addr = cm.get_asset_data_for_time_range(asset, "AdrActCnt", date1, date2)
dcrmove = cm.get_asset_data_for_time_range(asset, "TxTfrValAdjUSD", date1, date2)

df = cmdc.combo_convert(real_cap)
df1 = cmdc.combo_convert(mcap)
df2 = cmdc.combo_convert(addr)
df3 = cmdc.combo_convert(dcrmove)

df = df.merge(df1, on='date', how='left').merge(df2, on='date', how='left').merge(df3, on='date', how='left')

df.columns = ['date', 'realizedcap', 'marketcap', 'activeaddr', 'dcrmove']

df['Unrealized P/L'] = df['marketcap'] - df['realizedcap'] 

df['P/L Depletion'] = df['Unrealized P/L'] / df['dcrmove'].rolling(14).sum() 

df['Unrealized P/L Take'] = (df['dcrmove'].rolling(14).sum() * 5) + df['realizedcap']

print(df)

#plot
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(df['date'], df['Unrealized P/L'])
plt.fill_between(df['date'], df['Unrealized P/L'], where=df['Unrealized P/L'] > 0, facecolor='blue', alpha=0.25)
plt.fill_between(df['date'], df['Unrealized P/L'], where=df['Unrealized P/L'] < 0, facecolor='red', alpha=0.25)
plt.title("Unrealized P/L")
""" plt.axhline(100000000, color='r', linestyle=':')
plt.axhline(-100000000, color='r', linestyle=':') """
plt.grid()

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df['date'], df['marketcap'], label='Market Cap')
plt.plot(df['date'], df['realizedcap'], label='Realized Cap')
plt.plot(df['date'], df['Unrealized P/L Take'], label='Profit Taker', linestyle=':', color='r')
plt.title("Market Cap & Realized Cap")
plt.legend()
plt.yscale('log')
plt.grid()

plt.show()