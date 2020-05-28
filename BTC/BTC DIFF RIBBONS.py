import coinmetrics
import matplotlib.pyplot as plt
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
date_1 = "2011-01-01"
date_2 = "2020-05-27"

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

df['ribbonprice'] = df['PriceUSD'].rolling(200).mean() * (1 / df['ratio'])
df['ribbonprice2'] = df['PriceUSD'].rolling(128).mean() * (1 / df['ratio2'])
df['ribbonprice3'] = df['PriceUSD'].rolling(90).mean() * (1 / df['ratio3'])
df['ribbonprice4'] = df['PriceUSD'] * (1 / df['ratio4'])
df['ribbonprice5'] = df['PriceUSD'] * (1 / df['ratio5'])
df['ribbonprice6'] = df['PriceUSD'] * (1 / df['ratio6'])
df['ribbonprice7'] = df['ribbonprice3'] * 2

df['profitprice'] = df['PriceUSD'] - df['ribbonprice3']

df['profitmargin'] = df['profitprice'] / df['ribbonprice3']

print(df)

#plot
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('#E0E0E0')
fig.patch.set_alpha(0.7)
 
ax1.plot(df['date'], df['PriceUSD'], label='USD Price')
ax1.plot(df['date'], df['ribbonprice'], label='Ribbon Price', linestyle=':', color='g')
ax1.plot(df['date'], df['ribbonprice2'], label='Ribbon Price2', linestyle=':', color='g')
ax1.plot(df['date'], df['ribbonprice3'], label='Ribbon Price3', linestyle=':', color='g')
ax1.plot(df['date'], df['ribbonprice7'], label='Ribbon Price7', linestyle=':', color='r')
ax1.set_ylabel('USD Prices')
ax1.set_yscale('log')
ax1.grid()

ax2 = ax1.twinx()
line3 = ax2.plot(df['date'], df['profitmargin'], color='r')
ax2.set_ylabel('Miner P/L per Coin (%)')
ax2.fill_between(df['date'], df['profitmargin'], where=df['profitmargin'] > 0, facecolor='blue', alpha=0.15)
ax2.fill_between(df['date'], df['profitmargin'], where=df['profitmargin'] < 0, facecolor='red', alpha=0.15)
ax2.set_ylim(1.5*df['profitmargin'].min(), 2*df['profitmargin'].max())

plt.title("BTCUSD vs Mining Price")
fig.tight_layout()
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