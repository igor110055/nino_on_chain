from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime as dt
import cm_data_converter as cmdc
import coinmetrics 
import matplotlib.ticker as ticker
import matplotlib as mpl
import numpy as np

dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

#   TICKET DATA
ticketPrice = dcrdata.chart("ticket-price")
print(ticketPrice.keys())

# Convert to pandas
tix = pd.DataFrame(ticketPrice)

tix['t'] = pd.to_datetime(tix['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d')

tix = tix.drop(columns=['window'])

tix.columns = ['tixvol', 'tixprice', 'date']

# COINMETRICS DATA

cm = coinmetrics.Community()

# Add early price data

filename = 'DCR/DCR_data.xlsx'
df_early = pd.read_excel(filename)
early = df_early[['date', 'PriceUSD', 'PriceBTC', 'CapMrktCurUSD']].copy()
early['date'] = pd.to_datetime(early['date'], utc=True)
early.columns = ['date', 'dcrusd', 'dcrbtc', 'mcap']

# Pull data
# Pull data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-10-12"
metric = "PriceUSD"
metric1 = "PriceBTC"
metric2 = "CapMrktCurUSD"
metric3 = "CapRealUSD"
metric4 = "BlkSizeByte"

metriclist = [metric, metric1, metric2, metric3, metric4]

df = pd.DataFrame(columns=['date'])

for item in metriclist:
    df1 = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, item, date_1, date_2))
    df1.columns = ['date', item]
    df = df.merge(df1, on='date', how='outer')

df['date'] = df['date'].dt.strftime('%Y-%m-%d') #convert to string format for merging purposes

# MERGE DATASETS
df = tix.merge(df, on='date', how='left')

df['date'] = pd.to_datetime(df['date'], utc=True)

df = df.merge(early, on='date', how='left')
df = df.fillna(0)

df['PriceUSD'].mask(df['PriceUSD'] == 0, df['dcrusd'], inplace=True)
df['PriceBTC'].mask(df['PriceBTC'] == 0, df['dcrbtc'], inplace=True)
df['CapMrktCurUSD'].mask(df['CapMrktCurUSD'] == 0, df['mcap'], inplace=True)

df = df.drop(columns=['dcrusd', 'dcrbtc', 'mcap'])

#convert ticket price from atoms to dcr
atoms = 100000000
df['tixprice'] = df['tixprice'] / atoms

#metrics
df['dcrvol'] = df['tixprice'] * df['tixvol']
df['dcrvolcum'] = df['dcrvol'].cumsum()

df['dcrbtcvol'] = df['dcrvol'] * df['PriceBTC']
df['dcrusdvol'] = df['dcrvol'] * df['PriceUSD']

targets = [1,10,20,30,40,50,60,70,80,90,100,110,120]

for target in targets:
    df[str(target)] = np.where(target < df['PriceUSD'], df['dcrvol'], 0).cumsum() / df['dcrvolcum']

print(df)

# Plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.barh(df['PriceUSD'], df['dcrvol'], color='aqua', alpha=0.25)
ax1.tick_params(color='w', labelcolor='w')
ax1.set_facecolor('black')
ax1.set_title("PoS Contributed At Certain DCRUSD Prices", fontsize=20, fontweight='bold', color='w', y=1.08)
ax1.set_ylabel("DCRUSD", fontsize=20, fontweight='bold', color='w')
ax1.set_ylim(0.43, df['PriceUSD'].max() * 1.1)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax1.get_xaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = ax1.twiny()
ax2.plot(df['date'].iloc[:-2], df['PriceUSD'].iloc[:-2], color='w')
ax2.set_facecolor('black')
ax2.tick_params(color='w', labelcolor='w')
ax2.grid()
ax2.set_yscale('log')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax3 = plt.subplot(2,1,2)
ax3.plot(df['date'], df['1'], color='w', label="DCR in Tix > 1: " + str(round(df['1'].iloc[-2], 4)))
ax3.plot(df['date'], df['10'], color='lime', label="DCR in Tix 10>: " + str(round(df['10'].iloc[-2], 4)))
ax3.plot(df['date'], df['20'], color='aqua', label="DCR in Tix > 20: " + str(round(df['20'].iloc[-2], 4)))
ax3.plot(df['date'], df['40'], color='m', label="DCR in Tix > 40: " + str(round(df['40'].iloc[-2], 4)))
ax3.plot(df['date'], df['80'], color='r', label="DCR in Tix > 80: " + str(round(df['80'].iloc[-2], 4)))
ax3.legend()
ax3.tick_params(color='w', labelcolor='w')
ax3.set_facecolor('black')
ax3.set_title("% of Total DCR Ticket Volume Above Certain DCRUSD Prices", fontsize=20, fontweight='bold', color='w')
ax3.grid()
ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

plt.show() 