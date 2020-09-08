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
""" asset = "usdt" """
""" available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types) """

# List assets & dates

date_1 = "2017-01-01"
date_2 = "2020-09-08"

asset = "btc"
asset1 = "busd"
asset2 = "husd"
asset3 = "tusd"
asset4 = "usdc"
asset5 = "usdt"
asset6 = "usdt_eth"
asset7 = "usdt_trx"

#build dataset

btc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))
busd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "CapMrktCurUSD", date_1, date_2))
husd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset2, "CapMrktCurUSD", date_1, date_2))
tusd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset3, "CapMrktCurUSD", date_1, date_2))
usdc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset4, "CapMrktCurUSD", date_1, date_2))
usdt = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset5, "CapMrktCurUSD", date_1, date_2))
usdt_eth = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset6, "CapMrktCurUSD", date_1, date_2))
usdt_trx = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset7, "CapMrktCurUSD", date_1, date_2))

btc.columns = ['date', asset]
busd.columns = ['date', asset1]
husd.columns = ['date', asset2]
tusd.columns = ['date', asset3]
usdc.columns = ['date', asset4]
usdt.columns = ['date', asset5]
usdt_eth.columns = ['date', asset6]
usdt_trx.columns = ['date', asset7]

df = btc.merge(busd, on='date', how='left').merge(husd, on='date', how='left').merge(tusd, on='date', how='left').merge(usdc, on='date', how='left').merge(usdt, on='date', how='left').merge(usdt_eth, on='date', how='left').merge(usdt_trx, on='date', how='left')

#create metrics

df['ReserveCap'] = df.sum(axis=1)
df['CashCap'] = df['ReserveCap'] - df['btc']
df['ReserveRatio'] = df['btc'] / df['ReserveCap']
df['BuyPower'] = df['ReserveRatio'] / df['ReserveRatio'].rolling(30).mean()

print(df)

#plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'], df['btc'], color='w')
ax1.set_facecolor('black')
ax1.set_title("Bitcoin Market Cap", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_yscale('log')
ax1.grid()
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(df['date'], df['BuyPower'], color='w')
ax2.set_title("Buying Power", fontsize=20, fontweight='bold', color='w')
ax2.set_facecolor('black')
ax2.tick_params(color='w', labelcolor='w')
ax2.axhline(1.005, color='r', linestyle='dashed')
ax2.axhline(0.995, color='lime', linestyle='dashed')

plt.show()