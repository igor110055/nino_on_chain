# basic imports
import requests
import pandas as pd

# COINMETRICS
import coinmetrics
import cm_data_converter as cmdc
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter
from binance.client import Client

# api connect

api_key = 'ULgUTHU0vZODL2q4FmTHArsVy1iTJoDaqIMwSThKMKR7wvWZnDO2a2pxvVW9UEph'
api_secret = 'Jq2r0tvBv7QFEE72DObbWpRlvmSmJQIeSzFm4oAKNx3AW8mSOL17CM2wLt9yr0WU'

client = Client(api_key, api_secret)

# pull data
coin = 'DCRBTC'
date1 = "1 Jan, 2018"
date2 = "22 Sep, 2020"

df = pd.DataFrame(client.get_historical_klines(coin, Client.KLINE_INTERVAL_1DAY, date1, date2))
df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']

df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')    #format date
df['Open'] = pd.to_numeric(df['Open'])
df['Volume'] = pd.to_numeric(df['Volume'])
df['Quote Asset Volume'] = pd.to_numeric(df['Quote Asset Volume'])

# calc metrics

df['adjvol'] = df['Volume'] / df['Number of Trades']
df['btcadjvol'] = df['Quote Asset Volume'] / df['Number of Trades']

df['cumvol'] = df['Volume'].cumsum()
df['volshare'] = df['Volume'] / df['cumvol'].iloc[-1]
df['volsum'] = df['volshare'].rolling(10).sum()

print(df)

# plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2, 1, 1)
ax1.plot(df['Open Time'], df['Open'], color='w')
ax1.set_facecolor('black')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.set_title(coin.upper(), fontsize=20, fontweight='bold', color='w')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax2 = plt.subplot(2,1,2,sharex=ax1)
ax2.bar(df['Open Time'], df['volsum'], color='aqua')
ax2.set_facecolor('black')
ax2.tick_params(color='w', labelcolor='w')
ax2.grid()
ax2.set_title(coin.upper() + " - Amount Exchanged per Trade", fontsize=20, fontweight='bold', color='w')
""" ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

plt.show()