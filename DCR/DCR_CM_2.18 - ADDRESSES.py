import coinmetrics
import cm_data_converter as cmdc
import pandas as pd 
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker

cm = coinmetrics.Community()

# Pull data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-05-01"
date_2 = "2020-10-08"
metric = "AdrActCnt"
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

print(df)

# calc metrics

#Basic Address Metrics
df['addmean1'] = df['AdrActCnt'].rolling(56).mean()
df['addmean2'] = df['AdrActCnt'].rolling(142).mean()
df['addpct'] = df['addmean1'].pct_change(56)

#Market Cap Metrics
df['addmcap'] = df['CapMrktCurUSD'] / df['AdrActCnt']
df['28addmcap'] = df['addmcap'].rolling(28).mean()
df['142addmcap'] = df['addmcap'].rolling(142).mean()

#Realized Cap Metrics
df['addrealcap'] = df['CapRealUSD'] / df['AdrActCnt']
df['addrealpct'] = df['addrealcap'].pct_change(28)

#Data Metrics
df['byteperadd'] = df['BlkSizeByte'] / df['AdrActCnt']
df['byteperaddmean1'] = df['byteperadd'].rolling(28).mean()
df['byteperaddmean2'] = df['byteperadd'].rolling(84).mean()

# plot

name = "@permabullnino"
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'], df['addmean1'], color='w')
ax1.set_ylabel("Bytes per Address Used", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Bytes Added to Chain per Address", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
""" ax1.set_yscale('log') """
ax1.legend(edgecolor='w')
""" ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(df['date'], df['PriceBTC'], color='w')
""" ax2.plot(df['date'], df['CapMrktCurUSD'], color='w', label='Market Cap')
ax2.plot(df['date'], df['CapRealUSD'], color='lime', label='Realized Cap') """
ax2.set_ylabel("Decred Price", fontsize=20, fontweight='bold', color='w')
ax2.set_facecolor('black')
ax2.set_title("DCRBTC", fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.grid()
ax2.legend(edgecolor='w')
""" ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

plt.show()