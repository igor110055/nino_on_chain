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

available_data_types = cm.get_available_data_types_for_asset("btc")
print("available data types:\n", available_data_types)

# List assets & dates

date_1 = "2015-06-01"
date_2 = "2020-10-30"

asset = "btc"
asset1 = "busd"
asset2 = "husd"
asset3 = "tusd"
asset4 = "usdc"
asset5 = "usdt"
asset6 = "usdt_eth"
asset7 = "usdt_trx"
asset8 = "pax"

metric = "CapMrktCurUSD"

assetlist = [asset, asset1, asset2, asset3, asset4, asset5, asset6, asset7, asset8]
metriclist = [metric]

df = pd.DataFrame(columns=['date'])

for coin in assetlist:
    for item in metriclist: 
        df1 = cmdc.combo_convert(cm.get_asset_data_for_time_range(coin, item, date_1, date_2))
        df1.columns = ['date', coin + item]
        df = df.merge(df1, on='date', how='outer')

# Calc Metrics

df['StableCap'] = df.iloc[:, 2:9].sum(axis=1)
df['StableChg'] = df['StableCap'].diff(14)

print(df)

# Plot

name = "@permabullnino"
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
ax1.plot(df['date'], df['StableChg'], color='lime')
ax1.set_ylabel("Stable Coin Value", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Bitcoin Market Cap vs Monetary Premium Lines", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend(edgecolor='w')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = ax1.twinx()
ax2.plot(df['date'], df[asset+'CapMrktCurUSD'], color='w')
ax2.set_ylabel("Network Value", fontsize=20, fontweight='bold', color='w')
ax2.set_yscale('log')
ax2.tick_params(color='w', labelcolor='w')
ax2.legend(edgecolor='w')
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

plt.show()