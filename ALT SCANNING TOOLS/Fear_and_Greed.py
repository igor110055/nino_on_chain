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

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# Pull data
asset = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2018-02-01"
date_2 = "2020-09-21"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
price.columns = ['timestamp', 'btcusd']

# get data and convert to pandas
response = requests.get("https://api.alternative.me/fng/?limit=0")
response = response.json()

fg_data = response['data']
df = pd.DataFrame(fg_data)
df['value'] = df['value'].astype(int)

# convert dates and remove timeuntilupdate

df = df.drop(columns=['time_until_update'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', utc='True')
df = df.sort_values(by='timestamp')

# merge cm and fg data
df = df.merge(price, on='timestamp', how='left')
print(df)

# plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['timestamp'], df['value'], color='aqua')
ax1.set_title("Fear & Greed", fontsize=20, fontweight='bold', color='aqua')
ax1.set_facecolor('black')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.axhspan(20,60, color='w', alpha=0.3)

ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(df['timestamp'], df['btcusd'], color='w')
ax2.set_title("BTCUSD", fontsize=20, fontweight='bold', color='w')
ax2.set_facecolor('black')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.grid()
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

plt.show()
