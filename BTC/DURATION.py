import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib.ticker as ticker
import matplotlib as mpl

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for BTC.
asset = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

#fetch desired data
date_1 = "2011-01-01"
date_2 = "2020-10-26"

metric = "PriceUSD"
metric1 = "BlkCnt"

metriclist = [metric, metric1]

df = pd.DataFrame(columns=['date'])

for item in metriclist:
    df1 = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, item, date_1, date_2))
    df1.columns = ['date', item]
    df = df.merge(df1, on='date', how='outer')

# calc metrics

mins = 1440

df['blktime'] = mins / df['BlkCnt']
df['blktimeavg'] = df['blktime'].rolling(14).mean()
df['blktimeavg1'] = df['blktime'].rolling(70).mean()

print(df)

# Plot
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
ax1.plot(df['date'], df['blktimeavg1'], color='aqua', label='70 Day Blk Time Avg: ' + str(round(df['blktimeavg1'].iloc[-1], 2)))
ax1.fill_between(df['date'], df['blktimeavg1'], 10, where= df['blktimeavg1'] > 10, facecolor='red', alpha=0.5) 
ax1.fill_between(df['date'], df['blktimeavg1'], 10, where= df['blktimeavg1'] < 10, facecolor='lime', alpha=0.5) 
ax1.tick_params(color='w', labelcolor='w')
ax1.set_facecolor('black')
ax1.set_title("BTCUSD vs Average Block Times", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel("Minutes", fontsize=20, fontweight='bold', color='w')
ax1.grid()
ax1.legend()
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax2 = ax1.twinx()
ax2.plot(df['date'], df['PriceUSD'], color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')

plt.show()