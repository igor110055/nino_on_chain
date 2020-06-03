# GENERAL

from tinydecred.pydecred.dcrdata import DcrdataClient

dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import matplotlib.dates as dat
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# PULL DCR CM DATA & FORMAT

asset = "dcr"
date_1 = "2016-02-08"
date_2 = "2020-06-02"

pricebtc = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)

pricebtc = cmdc.combo_convert(pricebtc)

pricebtc['date'] = pd.to_datetime(pricebtc['date'], unit='s', utc=True).dt.strftime('%Y-%m-%d')
pricebtc.columns = ['date', 'DCRBTC']

# PULL DCRDATA

ticketPrice = dcrdata.chart("ticket-price")
df = pd.DataFrame(ticketPrice)

Stk_part = dcrdata.chart("stake-participation")
df1 = pd.DataFrame(Stk_part)

# FORMAT DCRDATA

df['t'] = pd.to_datetime(df['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d')
df.rename(columns={'t': 'date'}, inplace=True)

df['price'] = df['price'] / 100000000

df = df.groupby('date')['price'].mean()
df.columns = ['date', 'price']

df1['t'] = pd.to_datetime(df1['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d')
df1.rename(columns={'t': 'date'}, inplace=True)

df1['poolval'] = df1['poolval'] / 100000000
df1['circulation'] = df1['circulation'] / 100000000
df1 = df1.drop(columns=['axis', 'bin'])

# MERGE DATAFRAMES

df3 = df1.merge(pricebtc, on='date', how='left').merge(df, on='date', how='left')

df3['date'] = pd.to_datetime(df3['date'])

# CALC METRICS
target = 40960

df3['Tixinpool'] = df3['poolval'] / df3['price'].rolling(28).mean()
df3['Overflow'] = df3['Tixinpool'] - target
df3['Overflow14'] = df3['Overflow'].rolling(14).sum()
df3['dcroverflow'] = df3['Overflow'] * df3['price'].rolling(28).mean()
df3['btcoverflow'] = df3['dcroverflow'] * df3['DCRBTC']

print(df3)

#plot

plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(df3['date'], df3['Overflow'], label='TICKET POOL OVERFLOW')
plt.fill_between(df3['date'], df3['Overflow'], where=df3['Overflow'] > 0, facecolor='blue', alpha=0.25)
plt.fill_between(df3['date'], df3['Overflow'], where=df3['Overflow'] < 0, facecolor='red', alpha=0.25)
plt.title("TICKET POOL OVERFLOW")
plt.grid()
plt.legend()

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df3['date'], df3['DCRBTC'], label='DCRBTC PRICE')
plt.title("DCRBTC")
plt.legend()
plt.grid()
plt.yscale('log')

plt.show()