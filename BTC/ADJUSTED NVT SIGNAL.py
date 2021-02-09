# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib as mpl

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
""" asset = "usdt" """
""" available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types) """

# List assets & dates

date_1 = "2015-01-01"
date_2 = "2021-12-30"

asset = "btc"
asset1 = "busd"
asset2 = "husd"
asset3 = "tusd"
asset4 = "usdc"
asset5 = "usdt"
asset6 = "usdt_eth"
asset7 = "usdt_trx"
asset8 = "pax"

metric = "TxTfrValAdjUSD"
metric1 = "CapMrktCurUSD"
metric2 = "SplyCur"
metric3 = "PriceUSD"

assetlist = [asset, asset1, asset2, asset3, asset4, asset5, asset6, asset7, asset8]
assetlist1 = [asset]

metriclist = [metric]
metriclist1 = [metric1, metric2, metric3]

df = pd.DataFrame(columns=['date'])
dff = pd.DataFrame(columns=['date'])

for coin in assetlist:
    df1 = cmdc.combo_convert(cm.get_asset_data_for_time_range(coin, metric, date_1, date_2))
    df1.columns = ['date', coin+metric]
    df = df.merge(df1, on='date', how='outer')

for item in metriclist1:
    df2 = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, item, date_1, date_2))
    df2.columns = ['date', asset+item]
    df = df.merge(df2, on='date', how='outer')    

print(df)
######

df['Reserve Flow'] = df.iloc[:, 1:9].sum(axis=1)
df['Reserve Signal'] = df['btcCapMrktCurUSD'] / df['Reserve Flow'].rolling(window=90).mean()
df['Reserve Ratio'] = df['btcCapMrktCurUSD'] / df['Reserve Flow']
df['14 Day Avg Ratio'] = df['Reserve Ratio'].rolling(window=14).mean()
df['Reserve Top'] = df['Reserve Flow'].rolling(90).mean() * 75
df['Reserve Bottom'] = df['Reserve Flow'].rolling(90).mean() * 35
df['Reserve Middle'] = (df['Reserve Top'] + df['Reserve Bottom']) / 2

df['Reserve Top Price'] = df['Reserve Top'] / df['btcSplyCur']
df['Reserve Bottom Price'] = df['Reserve Bottom'] / df['btcSplyCur']
df['Reserve Middle Price'] = df['Reserve Middle'] / df['btcSplyCur']

print(df)

#plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2, 1, 1)
ax1.plot(df['date'], df['Reserve Signal'], label='Reserve Signal', color='aqua')
ax1.axhspan(37, 70, color='w', alpha=0.25)
ax1.set_yscale('log')
ax1.set_facecolor('black')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend()
ax1.set_title("Bitcoin Market Cap / Reserve Asset Flows", fontsize=20, fontweight='bold', color='w')

ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.plot(df['date'], df['btcPriceUSD'], label='BTCUSD Price: ' + str(round(df['btcPriceUSD'].iloc[-1], 2)), color='w')
ax2.plot(df['date'], df['Reserve Top Price'], label='Reserve Top: ' + str(round(df['Reserve Top Price'].iloc[-1], 2)), color='m')
ax2.plot(df['date'], df['Reserve Bottom Price'], label='Reserve Bottom: ' + str(round(df['Reserve Bottom Price'].iloc[-1], 2)), color='lime')
ax2.plot(df['date'], df['Reserve Middle Price'], label='Reserve Middle: ' + str(round(df['Reserve Middle Price'].iloc[-1], 2)), linestyle=':', color='aqua')
ax2.set_facecolor('black')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_title("BTC USD Price + Reserve Channels", fontsize=20, fontweight='bold', color='w')
ax2.set_yscale('log')
ax2.legend()
ax2.grid()
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

plt.show()