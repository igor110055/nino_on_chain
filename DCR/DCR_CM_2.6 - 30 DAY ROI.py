# Import the API
import coinmetrics
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "btc"
asset1 = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-07-29"

roi = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "ROI30d", date_1, date_2))
mcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))
altroi = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "ROI30d", date_1, date_2))
altmcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "CapMrktCurUSD", date_1, date_2))

df = roi.merge(mcap, on='date', how='left').merge(altmcap, on='date', how='left').merge(altroi, on='date', how='left')
df.columns = ['date', 'roi', 'mcap', 'altmcap', 'altroi']

print(df)

# plot 

name = "@permabullnino"
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
line1 = ax1.plot(df['date'], df['mcap'], color='w', label=asset.upper() + " MCAP")
ax1.set_ylabel("Network Value", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title(asset.upper() + " Market Cap vs ROI", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend(loc='upper right')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = ax1.twinx()
ax2.plot(df['date'], df['roi'], color='aqua', alpha=1, linestyle=':', label=asset.upper() + " ROI")
ax2.set_ylabel("30 Day ROI (%)", fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.legend(loc='upper left')
ax2.axhline(0, color='r', linestyle='dashed')
ax2.axhspan(40,50, color='w', alpha=0.5)
ax2.axhspan(-20,-30, color='lime', alpha=0.5)

ax3 = plt.subplot(2,1,2, sharex=ax1)
ax3.plot(df['date'], df['altmcap'], color='w', label=asset1.upper() + " MCAP")
ax3.set_ylabel("Network Value", fontsize=20, fontweight='bold', color='w')
ax3.set_facecolor('black')
ax3.set_title(asset1.upper() + " Market Cap vs ROI", fontsize=20, fontweight='bold', color='w')
ax3.set_yscale('log')
ax3.tick_params(color='w', labelcolor='w')
ax3.grid()
ax3.legend(loc='upper right')
ax3.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax4 = ax3.twinx()
ax4.plot(df['date'], df['altroi'], color='aqua', alpha=1, linestyle=':', label=asset1.upper() + " ROI")
ax4.set_ylabel("30 Day ROI (%)", fontsize=20, fontweight='bold', color='w')
ax4.tick_params(color='w', labelcolor='w')
ax4.legend(loc='upper left')
ax4.axhline(0, color='r', linestyle='dashed')
ax4.axhspan(-40,-50, color='lime', alpha=0.5)

plt.show()