# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter
import matplotlib as mpl

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# PULL DCR & BTC NTV, MVRV, & REALIZED PRICE DATA "2016-08-14"

asset = "btc"
date_1 = "2012-10-01"
date_2 = "2020-10-19"
metric = "BlkSizeByte"
metric1 = "FeeTotNtv"
metric2 = "PriceUSD"
metric3 = "TxCnt"
metric4 = "BlkCnt"
metric5 = "TxTfrValAdjNtv"

assetlist = [asset]
metriclist = [metric, metric1, metric2, metric3, metric4, metric5]

df = pd.DataFrame(columns=['date'])

for coin in assetlist:
    for item in metriclist: 
        df1 = cmdc.combo_convert(cm.get_asset_data_for_time_range(coin, item, date_1, date_2))
        df1.columns = ['date', coin + item]
        df = df.merge(df1, on='date', how='outer')

# Calc Metrics

df['feepertx'] = df['btcFeeTotNtv'] / df['btcTxCnt']

df['blksizeratio'] = df['btcBlkSizeByte'].rolling(30).mean() / df['btcBlkSizeByte'].rolling(90).mean()

df['tfrperblock'] = df['btcTxTfrValAdjNtv'] / df['btcBlkCnt']
df['tfrperblockratio'] = df['tfrperblock'].rolling(90).mean() / df['tfrperblock'].rolling(180).mean()

# Transfer Ribbons
df['ribbon30'] = df['tfrperblock'].rolling(30).mean()
df['ribbon60'] = df['tfrperblock'].rolling(60).mean()
df['ribbon90'] = df['tfrperblock'].rolling(90).mean()
df['ribbon120'] = df['tfrperblock'].rolling(120).mean()
df['ribbon150'] = df['tfrperblock'].rolling(150).mean()
df['ribbon180'] = df['tfrperblock'].rolling(180).mean()
df['ribbon270'] = df['tfrperblock'].rolling(270).mean()
df['ribbon360'] = df['tfrperblock'].rolling(360).mean()

print(df)

# Plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'], df['btcPriceUSD'], color='w')
ax1.set_ylabel("BTCUSD", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("BTCUSD", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_yscale('log')
ax1.grid()
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = plt.subplot(2,1,2)
ax2.plot(df['date'], df['ribbon30'], color='aqua')
""" ax2.plot(df['date'], df['ribbon60'], color='r')
ax2.plot(df['date'], df['ribbon90'], color='m')
ax2.plot(df['date'], df['ribbon120'], color='y') """
ax2.plot(df['date'], df['ribbon360'], color='lime')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_facecolor('black')
ax2.set_yscale('log')
ax2.set_ylabel("Transfer Amount", fontsize=20, fontweight='bold', color='w')
ax2.grid()
ax2.legend()
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

""" ax1 = plt.subplot(1,1,1)
ax1.plot(df['date'], df['btcPriceUSD'], color='w')
ax1.set_ylabel("BTCUSD", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Relative Data Added", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_yscale('log')

ax2 = ax1.twinx()
ax2.plot(df['date'], df['blksizeratio'], color='lime', linewidth=0.75)
ax2.set_yscale('log')
ax2.set_ylabel("Ratio", fontsize=20, fontweight='bold', color='w')
ax2.grid()
ax2.axhspan(0.95, 0.90, color='aqua', alpha=0.5)
ax2.axhspan(1.05, 1.10, color='aqua', alpha=0.5) """

""" ax1 = plt.subplot(1,1,1)
ax1.plot(df['date'], df['btcPriceUSD'], color='w')
ax1.set_ylabel("BTCUSD", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("BTC Moved per Block", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_yscale('log')

ax2 = ax1.twinx()
ax2.plot(df['date'], df['tfrperblockratio'], color='lime', linewidth=0.75)
ax2.set_yscale('log')
ax2.axhline(1, color='aqua', linestyle='dashed') """

plt.show()
