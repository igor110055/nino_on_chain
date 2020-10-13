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

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-10-12"
metric = "PriceBTC"
metric1 = "CapMrktCurUSD"
metric2 = "SplyCur"

assetlist = [asset, asset1]
metriclist = [metric, metric1, metric2]

df = pd.DataFrame(columns=['date'])

for coin in assetlist:
    for item in metriclist: 
        df1 = cmdc.combo_convert(cm.get_asset_data_for_time_range(coin, item, date_1, date_2))
        df1.columns = ['date', coin + item]
        df = df.merge(df1, on='date', how='outer')

# Calc Metrics

df['suppratio'] = df['btcSplyCur'] / df['dcrSplyCur']
df['eqsuppPriceBTC'] = df['suppratio'] * df['dcrPriceBTC']
df['mcapcomp'] = df['dcrCapMrktCurUSD'] / df['btcCapMrktCurUSD'] 

# Plot

name = "@permabullnino"
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
ax1.plot(df['date'], df['dcrPriceBTC'], color='w')
ax1.plot(df['date'], df['eqsuppPriceBTC'], color='lime')
ax1.plot(df['date'], df['mcapcomp'], color='aqua')
ax1.set_ylabel("DCRBTC", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("DCRBTC Price Comparisons", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend(edgecolor='w')
ax1.set_yscale('log')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

plt.show()