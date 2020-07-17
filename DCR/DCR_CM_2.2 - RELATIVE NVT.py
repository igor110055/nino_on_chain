# Import the API
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

# PULL DATA
asset = "dcr"
asset1 = "btc"
date1 = "2011-01-01"
date2 = "2020-07-16"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

dcrbtc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date1, date2))
dcrnvt = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "NVTAdj90", date1, date2))
btcnvt = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "NVTAdj90", date1, date2))
dcrusd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date1, date2))

df = dcrbtc.merge(dcrnvt, on='date', how='left').merge(btcnvt, on='date', how='left').merge(dcrusd, on='date', how='left')
df.columns = ['date', 'dcrbtc', 'dcrnvt', 'btcnvt', 'dcrusd']

# CALC METRICS

df['relnvt'] = df['dcrnvt'] / df['btcnvt']
df['relnvtprice'] = df['dcrbtc'] / df['relnvt']
df['relnvtprice2'] = 2 * df['relnvtprice']
df['relnvtprice4'] = 4 * df['relnvtprice']

# PLOT
name = "@permabullnino"
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
line1 = ax1.plot(df['date'], df['dcrbtc'], label=asset.upper() + 'BTC Market Traded Price', color='w')
line2 = ax1.plot(df['date'], df['relnvtprice'], label=asset.upper() + 'BTC NVT Price', linestyle='dashed', color='aqua')
line3 = ax1.plot(df['date'], df['relnvtprice2'], label='2x ' + asset.upper() + 'BTC NVT Price', linestyle='dashed', color='y')
line4 = ax1.plot(df['date'], df['relnvtprice4'], label='4x ' + asset.upper() + 'BTC NVT Price', linestyle='dashed', color='r')
ax1.set_ylabel(asset.upper() + "BTC", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title(asset.upper() + "BTC vs Relative NVT Price", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend(edgecolor='w')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(df['date'], df['relnvt'], color='w')
ax2.set_ylabel("Ratio Value", fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.set_title("Relative NVT Ratio", fontsize=20, fontweight='bold', color='w')
ax2.set_facecolor('black')
ax2.grid()
ax2.axhspan(1.05, 0.95, color='aqua', alpha=1)
ax2.axhline(2, color='y', alpha=1)
ax2.axhline(4, color='r', alpha=1)
for axis in [ax2.yaxis]:
    axis.set_major_formatter(ScalarFormatter())

plt.show()