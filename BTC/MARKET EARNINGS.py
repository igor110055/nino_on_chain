import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib as mpl

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for BTC
asset = "btc"
metric = "PriceUSD"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

#fetch desired data
date_1 = "2016-07-01"
date_2 = "2020-12-26"
df = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, metric, date_1, date_2))
df.columns = ['date', metric]

# Calc Metrics

df['move'] = df[metric].diff(1)
df['percentdailymove'] = df[metric].pct_change(1)
df['percent7'] = df['percentdailymove'].rolling(14).sum()
df['percent14'] = df['percentdailymove'].rolling(28).sum()
df['percent28'] = df['percentdailymove'].rolling(56).sum()
df['percentcombo'] = df['percent7'] + df['percent14'] + df['percent28']
print(df)

# PLOT

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1.bar(df['date'], df['percent28'], color='w', alpha=0.75)
ax1.set_facecolor('black')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_title("Daily Move " + asset.upper(), fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel("USD Moves", fontsize=20, fontweight='bold', color='w')
ax1.fill_between(df['date'], df['percent28'], where=df['percent28'] > 0, facecolor='lime', alpha=0.75)
ax1.fill_between(df['date'], df['percent28'], where=df['percent28'] < 0, facecolor='red', alpha=0.75)
ax1.grid()

ax2 = ax1.twinx()
ax2.plot(df['date'], df[metric], color='w', linewidth=2)
ax2.tick_params(color='w', labelcolor='w')
ax2.set_ylabel("Daily Price Close", fontsize=20, fontweight='bold', color='w')
ax2.set_yscale('log')
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

plt.show()