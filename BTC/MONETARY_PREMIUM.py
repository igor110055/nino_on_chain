import coinmetrics
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics.
asset = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#fetch desired data
date_1 = "2010-01-01"
date_2 = "2020-09-22"

isstot = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "IssTotUSD", date_1, date_2))
mkt = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))

df = isstot.merge(mkt, on='date', how='left')

df.columns = ['date', 'isstot', 'mkt']
#calc metrics 

df['rewardsum'] = df['isstot'].cumsum()

df['2'] = df['rewardsum'] * 2
df['4'] = df['rewardsum'] * 4
df['8'] = df['rewardsum'] * 8
df['16'] = df['rewardsum'] * 16
df['32'] = df['rewardsum'] * 32
df['64'] = df['rewardsum'] * 64

print(df)

# plot the data

name = "@permabullnino"
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
ax1.plot(df['date'], df['mkt'], color='w')
ax1.plot(df['date'], df['rewardsum'], color='aqua', linewidth=2)
ax1.plot(df['date'], df['2'], linestyle=':')
ax1.plot(df['date'], df['4'], linestyle=':')
ax1.plot(df['date'], df['8'], color='lime', linewidth=2)
ax1.plot(df['date'], df['16'], linestyle=':')
ax1.plot(df['date'], df['32'], linestyle=':')
ax1.plot(df['date'], df['64'],  color='m', linewidth=2)
ax1.fill_between(df['date'], df['32'], df['64'], where=df['64'] > df['32'], facecolor='m', alpha=0.5)
ax1.set_ylabel("Network Value", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Bitcoin Market Cap vs Monetary Premium Lines", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend(edgecolor='w')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

plt.show()