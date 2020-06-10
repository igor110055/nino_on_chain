import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Add early price data

filename = 'DCR/DCR_data.xlsx'
df_early = pd.read_excel(filename)
early = df_early[['date', 'PriceUSD']].copy()
early['date'] = pd.to_datetime(early['date'], utc=True)
early.columns = ['date', 'earlyusd']

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics.
asset = "btc"
asset1 = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

#fetch desired data
date_1 = "2016-02-08"
date_2 = "2020-06-08"

diff = cm.get_asset_data_for_time_range(asset, "DiffMean", date_1, date_2)
price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)

altdiff = cm.get_asset_data_for_time_range(asset1, "DiffMean", date_1, date_2)
altprice = cm.get_asset_data_for_time_range(asset1, "PriceUSD", date_1, date_2)

# clean CM data
diff = cmdc.combo_convert(diff)
price = cmdc.combo_convert(price)

altdiff = cmdc.combo_convert(altdiff)
altprice = cmdc.combo_convert(altprice)

# Merge
df = diff.merge(price, on='date', how='left').merge(altdiff, on='date', how='left').merge(altprice, on='date', how='left')

df.columns = ['date', 'difficulty', 'PriceUSD', 'altdifficulty', 'AltUSD']

# Merge early price data

df = df.merge(early, on='date', how='left')
df = df.fillna(0)

df['AltUSD'].mask(df['AltUSD'] == 0, df['earlyusd'], inplace=True)

# calc ribbons for both coins and mining prices
df['ribbon_200'] = df['difficulty'].rolling(window=200).mean()
df['ribbon_9'] = df['difficulty'].rolling(window=9).mean()

df['altribbon_200'] = df['altdifficulty'].rolling(window=200).mean()
df['altribbon_9'] = df['altdifficulty'].rolling(window=9).mean()

df['ratio'] = df['ribbon_9'] / df['ribbon_200']
df['altratio'] = df['altdifficulty'] / df['altribbon_200']

df['ribbonprice'] = df['PriceUSD'].rolling(90).mean() * (1 / df['ratio'])
df['altribbonprice'] = df['AltUSD'] * (1 / df['altratio'])

df['altbtcprice'] = df['AltUSD'] / df['PriceUSD']
df['altbtcribbon'] = df['altribbonprice'] / df['ribbonprice']
df['mixedprice'] = df['altribbonprice'] / df['PriceUSD']

df['priceratio'] = df['altbtcprice'] / df['altbtcribbon']
df['mixedratio'] = df['altbtcprice'] / df['mixedprice']

print(df)

# plot

fig = plt.figure()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(0.7)

ax1 = plt.subplot(2, 1, 1)
plt.plot(df['date'], df['altbtcprice'], label='Actual')
plt.plot(df['date'], df['mixedprice'], label='Mixed')
plt.rcParams['axes.facecolor'] = 'black'
plt.yscale('log')
plt.grid()
plt.title("Actual ALTBTC vs Mining ALTBTC")

plt.subplot(2,1,2, sharex=ax1) 
plt.plot(df['date'], df['mixedratio'], color='b')
plt.title("Mixed Ratio")
plt.yscale('log')
plt.grid(color='lime', linestyle='-')

plt.show()