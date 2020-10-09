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
date_2 = "2020-10-09"
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
df['dcrbtcvol'] = df['dcrvol'] * df['PriceBTC']
df['dcrusdvol'] = df['dcrvol'] * df['PriceUSD']

targets = [10,20,30]
for target in targets:
    for number in df['PriceUSD']:
        if number > target:
            df[str(target)] = np.sum(df['dcrvol']) 

print(df)

# Plot

a = np.histogram(df['PriceUSD'], weights=df['dcrvol'])

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
ax1.hist(a, bins='auto')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_facecolor('black')
ax1.set_title("DCRUSD / Lifetime Ticket Price", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.grid()

plt.show()