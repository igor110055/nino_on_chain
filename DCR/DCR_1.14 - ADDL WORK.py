# COINMETRICS
import coinmetrics
import numpy as np
import cm_data_converter as cmdc
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

# EARLY PRICE DATA
filename = 'DCR/DCR_data.xlsx'
df_early = pd.read_excel(filename)
early = df_early[['date', 'PriceUSD', 'PriceBTC', 'CapMrktCurUSD']].copy()
early['date'] = pd.to_datetime(pd.to_datetime(early['date'], utc=True).dt.strftime('%Y-%m-%d'))
early.rename(columns={'PriceUSD': 'dcrusd', 'PriceBTC': 'dcrbtc', 'CapMrktCurUSD': 'dcrmarketcap'}, inplace=True)

# COINMETRICS + MERGE EARLY

cm = coinmetrics.Community()

# Pull data
asset = "dcr"

date_1 = "2016-02-08"
date_2 = "2020-07-13"

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

# DCRDATA

df = pd.DataFrame(dcrdata.chart("chainwork"))
df['t'] = pd.to_datetime(pd.to_datetime(df['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d'))
df.rename(columns={'t': 'date'}, inplace=True)
df = df.drop(columns=['axis', 'bin'])

df = df.merge(price, on='date', how='left')

# Calc Metrics

df['addsupp'] = df['supply'].diff(1)
df['addsuppdollar'] = df['addsupp'] * df['PriceUSD']
df['powcumsum'] = (df['addsuppdollar'].cumsum()) * 0.6

df['addwork'] = df['work'].diff(1)
df['wtwork'] = df['addwork'] / df['work'].iloc[-1]
df['wtworksum'] = df['wtwork'].cumsum() # this is a check column to make sure wtwork adds up to 1

df['dailyworkval'] = (df['addsupp'] * df['PriceUSD']) / df['addwork']

print(df)

# Plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
ax1.plot(df['date'], df['mcap'], label='Market Cap', color='w')
ax1.plot(df['date'], df['powcumsum'], label='PoW Reward Sum', color='r')
ax1.set_ylabel("USD Value", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Market Cap vs Mining Tools", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend(loc='upper left')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax11 = ax1.twinx()
ax11.bar(df['date'], df['wtworksum'], color='aqua', alpha=0.5)

ax11.set_ylabel("Work Contributed Over Lifetime", fontsize=20, fontweight='bold', color='w')
ax11.tick_params(color='w', labelcolor='w')
ax11.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax11.axhline(0.5, color='m', linestyle='dashed')
ax11.axhline(0.1, color='m', linestyle='dashed')

plt.show()