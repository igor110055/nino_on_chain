from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime as dt
import cm_data_converter as cmdc
import coinmetrics 

dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

#   TICKET DATA
ticketPrice = dcrdata.chart("ticket-price")
print(ticketPrice.keys())

# Convert to pandas
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
date_2 = "2020-06-01"

price = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)

price = cmdc.combo_convert(price)

price['date'] = price['date'].dt.strftime('%Y-%m-%d')

# MERGE DATASETS

df = df.merge(price, on='date', how='left')

df['date'] = pd.to_datetime(df['date'])

df.rename(columns={'data': 'DCRBTC'}, inplace=True)

# Plot the data
fig = plt.figure()
fig.patch.set_facecolor('#E0E0E0')
fig.patch.set_alpha(0.7)

ax1 = plt.subplot(2,1,1)
plt.plot(df['date'], df['DCRBTC'])
plt.title("DCRBTC Price")
plt.yscale('log')
plt.grid()

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df['date'], df['rolling_7'], color='r')
plt.title("288 Block Rolling Sum of DCR Ticket Volume")
plt.grid()
""" plt.ylim(500, 950)
plt.axhspan(550, 600, color='g', alpha=0.10) """
plt.show()