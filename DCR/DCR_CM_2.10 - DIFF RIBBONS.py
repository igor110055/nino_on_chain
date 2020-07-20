import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib.ticker as ticker

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics.
asset = "zec"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

#fetch desired data
date_1 = "2010-01-01"
date_2 = "2020-07-20"

diff = cm.get_asset_data_for_time_range(asset, "DiffMean", date_1, date_2)
price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)

# clean CM data
diff = cmdc.combo_convert(diff)
price = cmdc.combo_convert(price)

# Merge
df = diff.merge(price, on='date', how='left')

df.columns = ['date', 'difficulty', 'PriceUSD']

# calc 200, 128, 90, 60, 40, 25, 14, 9 day ribbons
df['ribbon_200'] = df['difficulty'].rolling(window=200).mean()
df['ribbon_128'] = df['difficulty'].rolling(window=128).mean()
df['ribbon_90'] = df['difficulty'].rolling(window=90).mean()
df['ribbon_60'] = df['difficulty'].rolling(window=60).mean()
df['ribbon_40'] = df['difficulty'].rolling(window=40).mean()
df['ribbon_25'] = df['difficulty'].rolling(window=25).mean()
df['ribbon_14'] = df['difficulty'].rolling(window=14).mean()
df['ribbon_9'] = df['difficulty'].rolling(window=9).mean()

df['ratio'] = df['ribbon_9'] / df['ribbon_200']
df['ratio2'] = df['ribbon_9'] / df['ribbon_128']
df['ratio3'] = df['ribbon_9'] / df['ribbon_90']
df['ratio4'] = df['ribbon_9'] / df['ribbon_60']
df['ratio5'] = df['ribbon_9'] / df['ribbon_25']
df['ratio6'] = df['ribbon_9'] / df['ribbon_14']
df['ratio7'] = df['ribbon_90'] / df['ribbon_200']
df['ratio8'] = df['difficulty'] / df['ribbon_200']

df['ribbonprice'] = df['PriceUSD'].rolling(200).mean() * (1 / df['ratio'])
df['ribbonprice2'] = df['PriceUSD'].rolling(128).mean() * (1 / df['ratio2'])
df['ribbonprice3'] = df['PriceUSD'].rolling(90).mean() * (1 / df['ratio3'])
df['ribbonprice4'] = df['PriceUSD'] * (1 / df['ratio4'])
df['ribbonprice5'] = df['PriceUSD'] * (1 / df['ratio5'])
df['ribbonprice6'] = df['PriceUSD'] * (1 / df['ratio6'])
df['ribbonprice7'] = df['PriceUSD'] * (1 / df['ratio8'])
df['ribbonprice8'] = df['ribbonprice7'] * 1.25
df['ribbonprice9'] = df['ribbonprice7'] * .75

df['profitprice'] = df['PriceUSD'] - df['ribbonprice7']

df['profitmargin'] = df['profitprice'] / df['ribbonprice7']

print(df)

#plot
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'], df['PriceUSD'], label='USD Price', color='w')
ax1.plot(df['date'], df['ribbonprice7'], label='Ribbon Price', color='aqua')
ax1.set_facecolor('black')
ax1.set_ylabel('USD Prices', fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_title(asset.upper()+ "USD vs Mining Price", fontsize=20, fontweight='bold', color='w')
ax1.grid()
ax1.legend(loc='upper right')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

""" ax2 = ax1.twinx()
ax2.plot(df['date'], df['profitmargin'], color='aqua', linestyle=':')
ax2.set_ylabel('Miner P/L per Coin (%)', fontsize=20, fontweight='bold', color='w')
ax2.fill_between(df['date'], df['profitmargin'], where=df['profitmargin'] > 0, facecolor='aqua', alpha=0.4)
ax2.fill_between(df['date'], df['profitmargin'], where=df['profitmargin'] < 0, facecolor='red', alpha=1)
ax2.set_ylim(1.5*df['profitmargin'].min(), 3*df['profitmargin'].max())
ax2.tick_params(color='w', labelcolor='w')
ax2.legend(loc='upper left') """

ax3 = plt.subplot(2,1,2, sharex=ax1)
ax3.plot(df['date'], df['difficulty'], label='Difficulty', color='aqua')
ax3.plot(df['date'], df['ribbon_200'], label='200', color='lime')
ax3.plot(df['date'], df['ribbon_128'], label='128', color='aqua', alpha=0.5)
ax3.plot(df['date'], df['ribbon_90'], label='90', color='aqua', alpha=0.5)
ax3.plot(df['date'], df['ribbon_60'], label='60', color='aqua', alpha=0.5)
ax3.plot(df['date'], df['ribbon_40'], label='40', color='aqua', alpha=0.5)
ax3.plot(df['date'], df['ribbon_25'], label='25', color='aqua', alpha=0.5)
ax3.plot(df['date'], df['ribbon_14'], label='14', color='aqua', alpha=0.5)
ax3.plot(df['date'], df['ribbon_9'], label='9', color='aqua', alpha=0.5)
ax3.set_facecolor('black')
ax3.set_yscale('log')
ax3.tick_params(color='w', labelcolor='w')
ax3.set_title(asset.upper() + " Difficulty Ribbon", fontsize=20, fontweight='bold', color='w')
ax3.set_ylabel('Difficulty Target', fontsize=20, fontweight='bold', color='w')
ax3.grid()
ax3.legend(loc='best')

plt.show()

# EXTRA CODE TO PLOT OTHER THINGS

""" ax1 = plt.subplot(3, 1, 1)
plt.plot(df['date'], df['ribbon_200'], label='200')
plt.plot(df['date'], df['ribbon_128'], label='128')
plt.plot(df['date'], df['ribbon_90'], label='90')
plt.plot(df['date'], df['ribbon_60'], label='60')
plt.plot(df['date'], df['ribbon_40'], label='40')
plt.plot(df['date'], df['ribbon_25'], label='25')
plt.plot(df['date'], df['ribbon_14'], label='14')
plt.plot(df['date'], df['ribbon_9'], label='9')
plt.yscale('log')
plt.legend()
plt.grid()
plt.title("Difficulty Ribbons")

plt.subplot(3,1,2, sharex=ax1) 
plt.plot(df['date'], df['ratio'])
plt.title("Ribbon Ratio")
plt.yscale('log')
plt.grid() """