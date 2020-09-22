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

# pull data & format
coin = 'DCRBTC'

ob = client.get_order_book(symbol=coin)
bids = pd.DataFrame(ob['bids'])
asks = pd.DataFrame(ob['asks'])

bids.columns = [coin, 'Amount']
asks.columns = [coin, 'Amount']

bids[coin] = pd.to_numeric(bids[coin])
asks[coin] = pd.to_numeric(asks[coin])

bids['Amount'] = pd.to_numeric(bids['Amount'])
asks['Amount'] = pd.to_numeric(asks['Amount'])

# calc metrics

bids['bidorderbook'] = bids['Amount'].cumsum()
asks['askorderbook'] = asks['Amount'].cumsum()

print(asks)

# plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1.plot(asks[coin], asks['askorderbook'], color='r')
ax1.plot(bids[coin], bids['bidorderbook'], color='lime')
ax1.fill_between(asks[coin], asks['askorderbook'], where=asks['askorderbook'] > 0, facecolor='red', alpha=0.6)
ax1.fill_between(bids[coin], bids['bidorderbook'], where=bids['bidorderbook'] > 0, facecolor='lime', alpha=0.6)
ax1.set_facecolor('black')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.set_title(coin.upper() + " Orderbook", fontsize=20, fontweight='bold', color='w')

plt.show()