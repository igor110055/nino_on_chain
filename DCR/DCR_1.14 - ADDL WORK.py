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
date_2 = "2020-10-26"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
pricebtc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))
mcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))
supply = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "SplyCur", date_1, date_2))
realcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapRealUSD", date_1, date_2))
price = supply.merge(price, on='date', how='left').merge(pricebtc, on='date', how='left').merge(mcap, on='date', how='left').merge(realcap, on='date', how='left')
price['date'] = pd.to_datetime(pd.to_datetime(price['date'], unit='s', utc=True).dt.strftime('%Y-%m-%d'))
price.columns = ['date', 'supply', 'PriceUSD', 'PriceBTC', 'mcap', 'realcap']

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

days = 142 # change rolling value to look at different timeframes for work weighted prices

df['addsupp'] = df['supply'].diff(1)
df['addsuppdollar'] = df['addsupp'] * df['PriceUSD']
df['addsuppbtc'] = df['addsupp'] * df['PriceBTC']
df['powcumsum'] = (df['addsuppdollar'].cumsum()) * 0.6
df['btcpowcumsum'] = (df['addsuppbtc'].cumsum()) * 0.6

df['addwork'] = df['work'].diff(1)
df['addworkavg'] = df['addwork'].rolling(days).mean()
df['wtwork'] = df['addwork'] / df['work'].iloc[-1]
df['wtworksum'] = df['wtwork'].cumsum() # this is a check column to make sure wtwork adds up to 1

df['rollworksum'] = df['addwork'].rolling(days, min_periods=0).sum() 
df['rollwtwork'] = df['addwork'] / df['rollworksum'].shift(-1 * days)

df['dailyworkval'] = (df['PriceUSD']) * df['wtwork']
df['dcrdailyworkval'] = df['addsupp'] * df['wtwork']
df['btcdailyworkval'] = (df['PriceBTC']) * df['wtwork']
df['mcapworkval'] = df['mcap'] * df['wtwork']

df['rollworkval'] = (df['PriceUSD']) * df['rollwtwork']
df['dcrrollworkval'] = df['addsupp'] * df['rollwtwork']
df['btcrollworkval'] = (df['PriceBTC']) * df['rollwtwork']

df['usdsumworkval'] = df['dailyworkval'].cumsum()
df['btcsumworkval'] = df['btcdailyworkval'].cumsum()
df['mcapsumworkval'] = df['mcapworkval'].cumsum()

df['usdrollingwork'] = df['rollworkval'].rolling(days).sum()
df['btcrollingwork'] = df['btcrollworkval'].rolling(days).sum()

targets = [1,10,20,30,40,50,60,70,80,90,100,110,120]

for target in targets:
    df[str(target)] = np.where(target < df['PriceUSD'], df['addwork'], 0).cumsum() / df['work']

targetsbtc = [.001,.002,.003,.004,.005,.006,.007,.008,.009,.01,.011,.012,.013,.014]

for targeta in targetsbtc:
    df[str(targeta)] = np.where(targeta < df['PriceBTC'], df['addwork'], 0).cumsum() / df['work']

print(df)

# Plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

#DCRBTC VPVR

""" ax1 = plt.subplot(2,1,1)
ax1.barh(df['PriceBTC'], df['addwork'], color='aqua', alpha=0.25)
ax1.tick_params(color='w', labelcolor='w')
ax1.set_facecolor('black')
ax1.set_title("PoW Contributed At Certain DCRBTC Prices", fontsize=20, fontweight='bold', color='w', y=1.08)
ax1.set_ylabel("DCRBTC", fontsize=20, fontweight='bold', color='w')
ax1.set_ylim(df['PriceBTC'].min(), df['PriceBTC'].max() * 1.1)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax1.get_xaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = ax1.twiny()
ax2.plot(df['date'].iloc[:-2], df['PriceBTC'].iloc[:-2], color='w')
ax2.set_facecolor('black')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.grid()
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y))) """

ax3 = plt.subplot(1,1,1)
ax3.plot(df['date'], df['0.001'], color='w', label="PoW Contributed w/ DCRBTC > .001: " + str(round(df['0.001'].iloc[-2], 1)))
ax3.plot(df['date'], df['0.002'], color='lime', label="PoW Contributed w/ DCRBTC > .002: " + str(round(df['0.002'].iloc[-2], 4)))
ax3.plot(df['date'], df['0.004'], color='aqua', label="PoW Contributed w/ DCRBTC > .004: " + str(round(df['0.004'].iloc[-2], 4)))
ax3.plot(df['date'], df['0.006'], color='m', label="PoW Contributed w/ DCRBTC > .006: " + str(round(df['0.006'].iloc[-2], 4)))
ax3.plot(df['date'], df['0.008'], color='r', label="PoW Contributed w/ DCRBTC > .008: " + str(round(df['0.008'].iloc[-2], 4)))
ax3.legend()
ax3.tick_params(color='w', labelcolor='w')
ax3.set_facecolor('black')
ax3.set_title("% of Total PoW Contributed Above Certain DCRBTC Prices", fontsize=20, fontweight='bold', color='w')
ax3.grid()
ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

#DCRUSD VPVR
""" ax1 = plt.subplot(2,1,1)
ax1.barh(df['PriceUSD'], df['addwork'], color='aqua', alpha=0.25)
ax1.tick_params(color='w', labelcolor='w')
ax1.set_facecolor('black')
ax1.set_title("PoW Contributed At Certain DCRUSD Prices", fontsize=20, fontweight='bold', color='w', y=1.08)
ax1.set_ylabel("DCRUSD", fontsize=20, fontweight='bold', color='w')
ax1.set_ylim(df['PriceUSD'].min(), df['PriceUSD'].max() * 1.1)
ax1.set_xscale('log')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax1.get_xaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = ax1.twiny()
ax2.plot(df['date'].iloc[:-2], df['PriceUSD'].iloc[:-2], color='w')
ax2.set_facecolor('black')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.grid()
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax3 = plt.subplot(2,1,2, sharex=ax2)
ax3.plot(df['date'], df['1'], color='w', label="PoW Contributed w/ DCRUSD > $1: " + str(round(df['1'].iloc[-2], 4)))
ax3.plot(df['date'], df['10'], color='lime', label="PoW Contributed w/ DCRUSD > $10: " + str(round(df['10'].iloc[-2], 4)))
ax3.plot(df['date'], df['20'], color='aqua', label="PoW Contributed w/ DCRUSD > $20: " + str(round(df['20'].iloc[-2], 4)))
ax3.plot(df['date'], df['40'], color='m', label="PoW Contributed w/ DCRUSD > $40: " + str(round(df['40'].iloc[-2], 4)))
ax3.plot(df['date'], df['80'], color='r', label="PoW Contributed w/ DCRUSD > $80: " + str(round(df['80'].iloc[-2], 4)))
ax3.legend(loc='lower left')
ax3.tick_params(color='w', labelcolor='w')
ax3.set_facecolor('black')
ax3.set_title("% of Total PoW Contributed Above Certain DCRUSD Prices", fontsize=20, fontweight='bold', color='w')
ax3.grid()
ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y))) """

#### other charts
""" ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(df['date'].iloc[:-2], df['PriceUSD'].iloc[:-2], color='w')
ax2.set_facecolor('black')
ax2.tick_params(color='w', labelcolor='w')
ax2.grid()
ax2.set_title("DCRUSD", fontsize=20, fontweight='bold', color='w')
ax2.set_yscale('log')
ax2.axhline(1, color='w', linestyle='dashed')
ax2.axhline(10, color='lime', linestyle='dashed')
ax2.axhline(20, color='aqua', linestyle='dashed')
ax2.axhline(40, color='m', linestyle='dashed')
ax2.axhline(80, color='r', linestyle='dashed')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y))) """

""" ax1 = plt.subplot(1,1,1)
ax1.plot(df['date'], df['mcap'], label='Market Cap', color='w')
ax1.plot(df['date'], df['powcumsum'], label='PoW Reward Sum', color='r')
ax1.plot(df['date'], df['realcap'], label='Realized Cap', color='lime')
ax1.set_ylabel("USD Value", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.legend(loc='upper right')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax11 = ax1.twiny()
ax11.plot(df['wtworksum'], df['mcap'], color='aqua', alpha=1, label='Market Cap vs Work as Time') # work as time (twiny)
ax11.set_title("Market Cap vs Mining Tools\n", fontsize=20, fontweight='bold', color='w')
ax11.set_ylabel("Work Contributed Over Lifetime", fontsize=20, fontweight='bold', color='w')
ax11.tick_params(color='w', labelcolor='w')
ax11.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax11.grid()
ax11.legend(loc='upper left')

ax111 = ax1.twinx()
ax111.bar(df['date'], df['addwork'], color='c', alpha=0.7)
ax11.bar(df['date'], df['wtworksum'], color='aqua', alpha=0.5) # basic look for total work vs price need to use 
ax111.tick_params(color='w', labelcolor='w')
ax111.set_ylabel("Work Contributed per Day (Units = Exahash)", fontsize=20, fontweight='bold', color='w')
ax111.grid()
ax111.set_yscale('log')
ax111.set_ylim(1, 500000)
ax111.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

""" ax2 = plt.subplot(2,1,1)
ax2.plot(df['date'], df['usdsumworkval'], color='lime')
ax2.plot(df['date'], df['PriceUSD'], color='w')
ax2.plot(df['date'], df['usdrollingwork'], color='aqua')
ax2.set_title("DCRUSD vs Lifetime Work-Weighted Price", fontsize=20, fontweight='bold', color='w')
ax2.set_facecolor('black')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.grid()
ax2.set_ylim(df['PriceUSD'].min(), df['PriceUSD'].max()*1.3)
ax2.legend()
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax2.set_ylabel("DCRUSD Value", fontsize=20, fontweight='bold', color='w')

ax22 = plt.subplot(2,1,2)
ax22.plot(df['date'], df['btcsumworkval'], color='lime')
ax22.plot(df['date'], df['PriceBTC'], color='w')
ax22.plot(df['date'], df['btcrollingwork'], color='aqua')
ax22.set_title("DCRBTC vs Lifetime Work-Weighted Price", fontsize=20, fontweight='bold', color='w')
ax22.set_yscale('log')
ax22.grid()
ax22.tick_params(color='w', labelcolor='w')
ax22.set_facecolor('black')
ax22.set_ylim(df['PriceBTC'].min(), df['PriceBTC'].max()*1.3)
ax22.legend()
ax22.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax22.set_ylabel("DCRBTC Value", fontsize=20, fontweight='bold', color='w') """

plt.show()