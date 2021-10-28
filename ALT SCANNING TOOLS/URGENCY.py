import coinmetrics
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime as dt
import cm_data_converter as cmdc
import matplotlib.ticker as ticker
import matplotlib as mpl

cm = coinmetrics.Community()

# Pull data
asset = "btc"

date_1 = "2011-02-08"
date_2 = "2020-12-27"
metric = "PriceUSD"
metric1 = "PriceBTC"
metric2 = "FeeTotNtv"
metric3 = "BlkCnt"
metric4 = "SplyCur"

metriclist = [metric, metric1, metric2, metric3, metric4]

df = pd.DataFrame(columns=['date'])

for item in metriclist:
    df1 = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, item, date_1, date_2))
    df1.columns = ['date', item]
    df = df.merge(df1, on='date', how='outer')

# METRICS
day = 1440
target = 10

df['blktime'] = (day / df['BlkCnt']).rolling(14).mean()

df['blktimediff'] = df['blktime'] - target
df['urgency'] = df['blktimediff'] * df['FeeTotNtv']

print(df)

# PLOT

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(3,1,1)
ax1.plot(df['date'], df['PriceUSD'], color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_facecolor('black')
ax1.set_title("Fee Analysis", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.grid()
ax1.legend()
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax2 = plt.subplot(2,1,2)
ax2.plot(df['date'], df['urgency'], color='w', label='DCRUSD: ' + str(round(df['PriceUSD'].iloc[-3], 2))) 
ax2.tick_params(color='w', labelcolor='w')
ax2.set_facecolor('black')
""" ax2.set_yscale('log') """
ax2.grid()
ax2.legend(loc='lower right')

""" ax3 = plt.subplot(3,1,3)
ax3.plot(df['date'], df['PriceUSD'], color='w', label='DCRUSD: ' + str(round(df['PriceUSD'].iloc[-3], 2))) 
ax3.tick_params(color='w', labelcolor='w')
ax3.set_facecolor('black')
ax3.set_yscale('log')
ax3.grid()
ax3.legend(loc='lower right') """

plt.show()