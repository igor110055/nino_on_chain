# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
""" asset = "usdt" """
""" available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types) """

# List assets & dates

date_1 = "2017-01-01"
date_2 = "2021-12-30"

asset = "btc"
asset1 = "eth"

metric = "CapRealUSD"
metric1 = "CapMrktCurUSD"
metric2 = "PriceBTC"

assetlist = [asset]
assetlist1 = [asset1]

metriclist = [metric, metric1]
metriclist1 = [metric1, metric2]

df = pd.DataFrame(columns=['date'])

for thing in metriclist1:
    df1 = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, thing, date_1, date_2))
    df1.columns = ['date', asset1+thing]
    df = df.merge(df1, on='date', how='outer')

for item in metriclist:
    df2 = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, item, date_1, date_2))
    df2.columns = ['date', asset+item]
    df = df.merge(df2, on='date', how='left')    

print(df)
# Metric

df['RealProfit'] = df['btcCapMrktCurUSD'] - df['btcCapRealUSD']
df['AltSeason'] = df['RealProfit'] / df['ethCapMrktCurUSD']
df['AltTarget'] = df['AltSeason'] * df['ethPriceBTC']

#plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2, 1, 1)
""" ax1.plot(df['date'], df['RealProfit'], label='BTC Profit', color='aqua')
ax1.plot(df['date'], df['ethCapMrktCurUSD'], label='Eth Market Cap', color='w') """
ax1.plot(df['date'], df['ethPriceBTC'], label='ETHBTC Price: ' + str(round(df['ethPriceBTC'].iloc[-1],4)), color='aqua')
ax1.plot(df['date'], df['AltTarget'], label='Alt Target Price: ' + str(round(df['AltTarget'].iloc[-1],4)), color='lime')
ax1.set_facecolor('black')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_yscale('log')
ax1.grid()
ax1.legend(loc='upper middle')
ax1.set_title("ETHBTC Price", fontsize=20, fontweight='bold', color='w')
ax1.set_ylim(df['ethPriceBTC'].min(), df['ethPriceBTC'].max())
""" ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

""" ax11 = ax1.twinx()
ax11.plot(df['date'], df['btcCapMrktCurUSD'], label='BTC Market Cap: ' + str(round(df['btcCapMrktCurUSD'].iloc[-1] / 1000000000,2)) + ' Billion', color='w')
ax11.tick_params(color='w', labelcolor='w')
ax11.legend(loc='lower middle')
ax11.set_yscale('log')
ax11.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

ax2 = plt.subplot(2, 1, 2)
ax2.plot(df['date'], df['AltSeason'], label='Alt Season Ratio: ' + str(round(df['AltSeason'].iloc[-1],3)), color='aqua')
ax2.set_facecolor('black')
""" ax2.set_yscale('log') """
ax2.tick_params(color='w', labelcolor='w')
ax2.grid()
ax2.legend(loc='lower left')
ax2.axhline(1, color='r')
ax2.axhline(4, color='lime')
ax2.set_ylim(df['AltSeason'].min(), 6)
ax2.set_title("Alt Season Ratio", fontsize=20, fontweight='bold', color='w')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

""" ax3 = ax2.twinx()
ax3.plot(df['date'], df['RealProfit'], label='Absolute Profit: ' + str(round(df['RealProfit'].iloc[-1] / 1000000000,2)) + ' Billion', color='w')
ax3.tick_params(color='w', labelcolor='w')
ax3.legend(loc='upper left')
ax3.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

plt.show()