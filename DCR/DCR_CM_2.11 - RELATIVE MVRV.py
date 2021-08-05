# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

from tinydecred.pydecred.dcrdata import DcrdataClient
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# PULL DCR & BTC NTV, MVRV, & REALIZED PRICE DATA "2016-08-14"

asset = "ltc"
asset1 = "btc"
date_1 = "2015-01-01"
date_2 = "2021-12-30"
metric = "SplyCur"
metric1 = "PriceBTC"
metric2 = "PriceUSD"
metric3 = "CapMVRVCur"
metric4 = "CapRealUSD"

assetlist = [asset, asset1]
metriclist = [metric, metric1, metric2, metric3, metric4]

df = pd.DataFrame(columns=['date'])

for coin in assetlist:
    for item in metriclist: 
        df1 = cmdc.combo_convert(cm.get_asset_data_for_time_range(coin, item, date_1, date_2))
        df1.columns = ['date', coin + item]
        df = df.merge(df1, on='date', how='outer')

# Pull DCRDATA
atoms = 100000000
Stk_part = pd.DataFrame(dcrdata.chart("stake-participation"))
Stk_part = Stk_part.drop(columns=['axis', 'bin'])
Stk_part.columns = ['circulation', 'poolval', 'date']

Stk_part['date'] = pd.to_datetime(Stk_part['date'], unit='s', utc=True)
Stk_part['circulation'] = Stk_part['circulation'] / atoms
Stk_part['poolval'] = Stk_part['poolval'] / atoms

# Merge Data

df = df.merge(Stk_part, on='date', how='left')

# CALC REALTIVE VALUE RATIOS

df['adjpart'] = df['poolval'] / df['circulation']   #stake pool participation

df['assetrealprice'] = df[asset+'CapRealUSD'] / df[asset+'SplyCur']
df['asset1realprice'] = df[asset1+'CapRealUSD'] / df[asset1+'SplyCur']
df['assetbtcrealbuypow'] = df['assetrealprice'] / df[asset1+'PriceUSD'].rolling(21).mean()
df['buypowbottom'] = (1 - df['adjpart']) * df['assetbtcrealbuypow']
df['buypowtop'] = (1 / df['adjpart']) * df['assetbtcrealbuypow']

df['rel_realprice'] = df['assetrealprice'] / df['asset1realprice']
df['rel_real'] = df[asset+'CapRealUSD'] / df[asset1+'CapRealUSD']
df['rel_mvrv'] = df[asset+'CapMVRVCur'] / df[asset1+'CapMVRVCur']

# CALC RELATIVE VALUE PRICES

df['buypowratio'] = df[asset+'PriceBTC'] / df['assetbtcrealbuypow']
df['REALRATIO'] = df['assetbtcrealbuypow'] / df['rel_realprice']
df['MVRVcomp'] = df[asset+'CapMVRVCur'] / df['buypowratio']
df['btc21'] = df[asset1+'PriceUSD'].rolling(21).mean()

df['rel_mvrv_price'] = df[asset+'PriceBTC'] / df['rel_mvrv']
df['mid_point'] = 0.7 * df['rel_realprice']

df['ocratio'] = df[asset+'PriceBTC'] / df['rel_real']
df['dcrratioprice'] = df['rel_realprice'] * 0.42
df['ocratio142'] = df['ocratio'].rolling(142).mean()
df['rel_mvrv142'] = df['rel_mvrv'].rolling(142).mean()

# SEND TO EXCEL
#df.to_excel('Relative Value Prices.xlsx')

print(df)

# PLOT VALUES

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

""" ax11 = plt.subplot(2,1,1)
ax11.plot(df['date'], df[asset1+'PriceUSD'], label= asset1.upper() + 'Market Traded Price: ' + str(round(df[asset1+'PriceUSD'].iloc[-1],2)), color='w')
ax11.plot(df['date'], df['asset1realprice'], label= asset1.upper() + ' Realized Price :' + str(round(df['asset1realprice'].iloc[-1],2)), color='m')
ax11.plot(df['date'], df['btc21'], label= asset1.upper() + ' Realized Price :' + str(round(df['asset1realprice'].iloc[-1],2)), color='m')
ax11.set_ylabel(asset1.upper() + "USD", fontsize=20, fontweight='bold', color='w')
ax11.set_facecolor('black')
ax11.set_title("Realized Price vs " + asset1.upper() + "USD", fontsize=20, fontweight='bold', color='w')
ax11.set_yscale('log')
ax11.tick_params(color='w', labelcolor='w')
ax11.grid()
ax11.legend()
ax11.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y))) """

ax1 = plt.subplot(1,1,1)
ax1.plot(df['date'], df[asset+'PriceBTC'], label= asset.upper() + 'BTC Market Traded Price: ' + str(round(df[asset+'PriceBTC'].iloc[-1],5)), color='w')
ax1.plot(df['date'], df['rel_realprice'], label= asset.upper() + ' Realized Price / BTC Realized Price :' + str(round(df['rel_realprice'].iloc[-2],5)), color='lime')
""" ax1.plot(df['date'], df['dcrratioprice'], label='Historical Bottom Zone: ' + str(round(df['dcrratioprice'].iloc[-1],5)), color='aqua')
ax1.plot(df['date'], df['assetbtcrealbuypow'], label='DCR Realized Price / BTCUSD.Mean(21 Days): ' + str(round(df['assetbtcrealbuypow'].iloc[-1],5)), color='m') """
ax1.set_ylabel(asset.upper() + 'BTC', fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Relative Value Prices", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend()
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

""" ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.plot(df['date'], df['MVRVcomp'], color='w')
ax2.set_facecolor('black')
ax2.set_title("Compare MVRV Ratios", fontsize=20, fontweight='bold', color='w')
ax2.set_ylabel("Ratio Value", fontsize=20, fontweight='bold', color='w')
ax2.axhline(1, color='r', linestyle='dashed')
ax2.axhline(1.15, color='lime', linestyle='dashed')
ax2.axhline(0.85, color='aqua', linestyle='dashed')
ax2.legend()
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.grid()
for axis in [ax2.yaxis]:
    axis.set_major_formatter(ScalarFormatter()) """ 

""" ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.plot(df['date'], df['rel_mvrv'], color='w')
ax2.plot(df['date'], df['rel_mvrv142'], color='m')
ax2.plot(df['date'], df['REALRATIO'], color='aqua')
ax2.set_facecolor('black')
ax2.set_title("Relative MVRV Ratio", fontsize=20, fontweight='bold', color='w')
ax2.set_ylabel("Ratio Value", fontsize=20, fontweight='bold', color='w')
ax2.axhspan(1.05, 0.95, color='r', alpha=0.4)
ax2.axhspan(.45, 0.4, color='w', alpha=0.4)
ax2.legend()
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.grid()
for axis in [ax2.yaxis]:
    axis.set_major_formatter(ScalarFormatter()) """

""" ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'], df[asset+'PriceBTC'], label= asset.upper() + 'BTC Market Traded Price: ' + str(round(df[asset+'PriceBTC'].iloc[-1],5)), color='w')
ax1.plot(df['date'], df['assetbtcrealbuypow'], label='Buy Power Price: ' + str(round(df['assetbtcrealbuypow'].iloc[-1],5)), color='m')
ax1.plot(df['date'], df['buypowtop'], label='Buy Power Price: ' + str(round(df['buypowtop'].iloc[-1],5)), color='red')
ax1.plot(df['date'], df['buypowbottom'], label='Buy Power Price: ' + str(round(df['buypowbottom'].iloc[-1],5)), color='lime')
ax1.set_ylabel("DCRBTC", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Relative Value Prices", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend()
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y))) """

""" ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.plot(df['date'], df['buypowratio'], color='w')
ax2.set_facecolor('black')
ax2.set_title("DCRBTC / DCRBTC Realized Price (MVRV) Ratio", fontsize=20, fontweight='bold', color='w')
ax2.set_ylabel("Ratio Value", fontsize=20, fontweight='bold', color='w')
ax2.legend()
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.grid()
for axis in [ax2.yaxis]:
    axis.set_major_formatter(ScalarFormatter()) """

plt.show()