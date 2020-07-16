# COINMETRICS
import coinmetrics
import cm_data_converter as cmdc
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

# COINMETRICS + MERGE EARLY

cm = coinmetrics.Community()

# Pull data
asset = "dcr"

date_1 = "2016-02-08"
date_2 = "2020-07-15"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
pricebtc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))
supply = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "SplyCur", date_1, date_2))
blk = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "BlkCnt", date_1, date_2))
price = supply.merge(price, on='date', how='left').merge(pricebtc, on='date', how='left').merge(blk, on='date', how='left')
price['date'] = pd.to_datetime(pd.to_datetime(price['date'], unit='s', utc=True).dt.strftime('%Y-%m-%d'))

price.columns = ['date', 'Supply', 'PriceUSD', 'PriceBTC', 'BlkCnt']

# DCRDATA

df = pd.DataFrame(dcrdata.chart("ticket-price"))
df['t'] = pd.to_datetime(pd.to_datetime(df['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d'))
df.rename(columns={'t': 'date', 'price': 'tixprice', 'count': 'volume'}, inplace=True)
df['tixprice'] = df['tixprice'] / 100000000
df = df.merge(price, on='date', how='left')

# Calc Metrics / Format Data

tickets = 5
pos = 0.3

df['window'] = tickets * df['window']
df['suppchg'] = df['Supply'].diff(1)
df['posrew'] = (df['suppchg'] * pos) / df['BlkCnt']
df['tixrew'] = df['posrew'] / tickets
df['tixror'] = df['tixrew'] / df['tixprice']

df = df[df.tixror != 0]

# CALC FUNDING RATE
days = 28

df['fundrate'] = df['tixror'] - df['tixror'].rolling(days).mean()
df['fundzscore'] = (df['fundrate'] - df['fundrate'].rolling(days).mean()) / df['fundrate'].rolling(days).std()
df['fundsum'] = df['fundzscore'].rolling(14).sum()

print(df)

# PLOT

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
ax1.plot(df['date'], df['PriceBTC'], color='w')
ax1.set_ylabel("Price", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("DCRBTC vs Funding Rates", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend()
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax11 = ax1.twinx()
ax11.bar(df['date'], df['fundsum'], alpha=0)
ax11.fill_between(df['date'], df['fundsum'], where=df['fundsum'] > 0, facecolor='red', alpha=0.7)
ax11.fill_between(df['date'], df['fundsum'], where=df['fundsum'] < 0, facecolor='lime', alpha=0.7)
ax11.set_ylabel("Funding Rate Z-Scores", fontsize=20, fontweight='bold', color='w')
ax11.tick_params(color='w', labelcolor='w')
ax11.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax11.axhline(-15, color='aqua', linestyle='dashed')
ax11.axhline(15, color='aqua', linestyle='dashed')
# toggle top and bottom to 0.74 and 0.26 respectively for best view

""" ax2 = plt.subplot(2,1,2)
ax2.plot(df['date'], df['PriceBTC'], color='w')
ax2.set_ylabel("Price", fontsize=20, fontweight='bold', color='w')
ax2.set_facecolor('black')
ax2.set_title("DCRBTC vs Funding Rates", fontsize=20, fontweight='bold', color='w')
ax2.set_yscale('log')
ax2.tick_params(color='w', labelcolor='w')
ax2.grid()
ax2.legend()
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax22 = ax2.twinx()
ax22.bar(df['date'], df['fundsum'], alpha=0)
ax22.fill_between(df['date'], df['fundzscore'], where=df['fundsum'] > 0, facecolor='red', alpha=0.7)
ax22.fill_between(df['date'], df['fundzscore'], where=df['fundsum'] < 0, facecolor='lime', alpha=0.7)
ax22.set_ylabel("Funding Rate Z-Score", fontsize=20, fontweight='bold', color='w')
ax22.set_ylim(-3, 3)
ax22.tick_params(color='w', labelcolor='w')
ax22.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y))) """

plt.show()