import coinmetrics
import cm_data_converter as cmdc
import pandas as pd 
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker

cm = coinmetrics.Community()

# Pull data
asset = "btc"
asset1 = "dcr"
asset2 = "eth"
asset3 = "dash"
asset4 = "bsv"
asset5 = "ltc"
asset6 = "bch"
asset7 = "xmr"
asset8 = "zec"
asset9 = "btg"
asset10 = "etc"
asset11 = "doge"

assetlist = [asset, asset1, asset2, asset3, asset4, asset5, asset6, asset7, asset8, asset9, asset10, asset11]

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2013-01-01"
date_2 = "2020-07-30"
metric = "CapMrktCurUSD"

df = pd.DataFrame(columns=['date'])

for coin in assetlist:
    mcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(coin, metric, date_1, date_2))
    mcap.columns = ['date', coin]
    df = df.merge(mcap, on='date', how='outer')

# calc metrics

df['moneycap'] = df.sum(axis=1)
df['dominance'] = df['btc'] / df['moneycap']
df['dcrdominance'] = df['dcr'] / df['moneycap']

print(df)

# plot

name = "@permabullnino"
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
line1 = ax1.plot(df['date'], df['dominance'], color='w')
ax1.set_ylabel("Dominance (%)", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Bitcoin Crypto-Money Dominance", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend(edgecolor='w')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax11 = ax1.twinx()
ax11.plot(df['date'], df['moneycap'], color='lime')
ax11.set_ylabel("Crypto-Money Cap", fontsize=20, fontweight='bold', color='w')
ax11.tick_params(color='w', labelcolor='w')
ax11.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
ax11.legend(loc='upper left')
ax11.set_yscale('log')

ax2 = plt.subplot(2,1,2, sharex=ax1)
line2 = ax2.plot(df['date'], df['dcrdominance'], color='w')
ax2.set_ylabel("Dominance (%)", fontsize=20, fontweight='bold', color='w')
ax2.set_facecolor('black')
ax2.set_title("Decred Crypto-Money Dominance", fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.grid()
ax2.legend(edgecolor='w')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax22 = ax2.twinx()
ax22.plot(df['date'], df['moneycap'], color='lime')
ax22.set_ylabel("Crypto-Money Cap", fontsize=20, fontweight='bold', color='w')
ax22.tick_params(color='w', labelcolor='w')
ax22.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
ax22.legend(loc='upper left')
ax22.set_yscale('log')

plt.show()
