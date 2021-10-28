from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime as dt
import cm_data_converter as cmdc
import coinmetrics 
import matplotlib.ticker as ticker

dcrdata = DcrdataClient("https://explorer.dcrdata.org/market")

#   TICKET DATA
ticketPrice = dcrdata.chart('depth')
print(ticketPrice.keys())

""" # Convert to pandas
df = pd.DataFrame(ticketPrice)

df['t'] = pd.to_datetime(df['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d')

df = df.drop(columns=['window'])

df.columns = ['tixvol', 'tixprice', 'date']

# Get 7-Day (14 period) rolling average
df['rolling_7'] = df['tixvol'].rolling(window=14).mean()
df['rolling_28'] = df['tixvol'].rolling(window=56).mean()
df['rollingsum'] = df['tixvol'].rolling(window=2).sum()

# COINMETRICS DATA

cm = coinmetrics.Community()

# Pull data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2021-12-30"

price = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)

price = cmdc.combo_convert(price)

price['date'] = price['date'].dt.strftime('%Y-%m-%d')

# MERGE DATASETS

df = df.merge(price, on='date', how='left')

df['date'] = pd.to_datetime(df['date'])

df.rename(columns={'data': 'DCRBTC'}, inplace=True)

print(df)

# Plot the data
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'], df['DCRBTC'], color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_facecolor('black')
ax1.set_title("DCRBTC Price", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.axhspan(.0105, .0095, color='lime', alpha=0.75)
ax1.axhspan(.0016, .0014, color='m', alpha=0.75)
ax1.axhspan(.004, .0039, color='y', alpha=0.75)
ax1.grid()
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(df['date'], df['rolling_7'], color='aqua')
ax2.set_facecolor('black')
ax2.set_ylabel('Ticket Volume', fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_title("7-Day Rolling Average DCR Ticket Volume", fontsize=20, fontweight='bold', color='w')
ax2.axhline(720, color='y', linestyle='dashed')
ax2.grid()
ax2.set_ylim(500, 950)
ax2.axhspan(550, 600, color='w', alpha=0.5)

plt.show() """