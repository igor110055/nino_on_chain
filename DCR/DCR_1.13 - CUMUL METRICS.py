# COINMETRICS
import coinmetrics
import cm_data_converter as cmdc
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

# GENERAL

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

# Add early price data

filename = 'DCR/DCR_data.xlsx'
df_early = pd.read_excel(filename)
early = df_early[['date', 'PriceUSD', 'PriceBTC', 'CapMrktCurUSD']].copy()
early['date'] = pd.to_datetime(pd.to_datetime(early['date'], utc=True).dt.strftime('%Y-%m-%d'))
early.rename(columns={'PriceUSD': 'dcrusd', 'PriceBTC': 'dcrbtc', 'CapMrktCurUSD': 'dcrmarketcap'}, inplace=True)

# COINMETRICS

cm = coinmetrics.Community()

# Pull data
asset = "dcr"

date_1 = "2016-02-08"
date_2 = "2020-07-10"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
pricebtc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))
mcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))
supply = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "SplyCur", date_1, date_2))
price = supply.merge(price, on='date', how='left').merge(pricebtc, on='date', how='left').merge(mcap, on='date', how='left')
price['date'] = pd.to_datetime(pd.to_datetime(price['date'], unit='s', utc=True).dt.strftime('%Y-%m-%d'))
price.columns = ['date', 'supply', 'PriceUSD', 'PriceBTC', 'mcap']

price = price.merge(early, on='date', how='left')
price = price.fillna(0)

price['PriceUSD'].mask(price['PriceUSD'] == 0, price['dcrusd'], inplace=True, axis=0)
price['PriceBTC'].mask(price['PriceBTC'] == 0, price['dcrbtc'], inplace=True, axis=0)
price['mcap'].mask(price['mcap'] == 0, price['dcrmarketcap'], inplace=True, axis=0)
price = price.drop(columns=['dcrusd', 'dcrusd', 'dcrbtc', 'dcrmarketcap'])

#   TICKET DATA
ticketPrice = dcrdata.chart("ticket-price")
df = pd.DataFrame(ticketPrice)

df1 = pd.DataFrame(dcrdata.chart("chainwork"))
df2 = pd.DataFrame(dcrdata.chart("blockchain-size"))

# convert atoms to dcr, calc dcr in tix vol, and convert to datetime
df['price'] = df['price'] / 100000000
df['dcrtixvol'] = df['price'] * df['count'] 

df['t'] = pd.to_datetime(pd.to_datetime(df['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d'))
df.rename(columns={'t': 'date'}, inplace=True)

df1['t'] = pd.to_datetime(pd.to_datetime(df1['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d'))
df1.rename(columns={'t': 'date'}, inplace=True)
df1 = df1.drop(columns=['axis', 'bin'])

df2['t'] = pd.to_datetime(pd.to_datetime(df2['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d'))
df2.rename(columns={'t': 'date'}, inplace=True)
df2 = df2.drop(columns=['axis', 'bin'])

df = df.merge(df1, on='date', how='left').merge(df2, on='date', how='left').merge(price, on='date', how='left')

# Calc Metrics

df['cumtix'] = df['count'].cumsum()
df['cumdcrtix'] = df['dcrtixvol'].cumsum()
df['valpertix'] = df['mcap'] / df['cumtix']
df['valperdcrtix'] = df['mcap'] / df['cumdcrtix']

df['valperwork'] = df['mcap'] / df['work']

df['valperbyte'] = df['mcap'] / df['size']

print(df)

# plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1, 1, 1)
ax1.plot(df['date'], df['valpertix'], label='Val Stored / Tix', color='aqua')
ax1.plot(df['date'], df['PriceUSD'], label='Price USD', color='w')
ax1.plot(df['date'], df['valperdcrtix'], label='Val Stored / DCR in Tix', color='lime')
ax1.plot(df['date'], df['valperbyte'], label='Val Stored / Byte', color='r')
ax1.plot(df['date'], df['valperwork'], label='Val Stored / Exahash', color='orange')
ax1.set_facecolor('black')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_yscale('log')
ax1.grid()
ax1.set_title("Lifetime Value Metrics vs USD Price", fontsize=20, fontweight='bold', color='w')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax1.set_ylabel("USD Value", fontsize=20, fontweight='bold', color='w')
ax1.legend()

""" ax2 = plt.subplot(2,1,2, sharex=ax1) 
ax2.plot(df['date'], df['mixedratio'], color='aqua')
ax2.set_facecolor('black')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_title("Mixed Ratio", fontsize=20, fontweight='bold', color='w')
ax2.set_yscale('log')
ax2.set_ylabel("Ratio Value", fontsize=20, fontweight='bold', color='w')
ax2.grid()
for axis in [ax2.yaxis]:
    axis.set_major_formatter(ScalarFormatter()) """

plt.show()