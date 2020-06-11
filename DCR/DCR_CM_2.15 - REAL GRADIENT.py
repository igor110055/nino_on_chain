import coinmetrics
import cm_data_converter as cmdc
import pandas as pd 
from matplotlib import pyplot as plt
import matplotlib as mpl

cm = coinmetrics.Community()

# Pull data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-06-09"

mcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))
realcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapRealUSD", date_1, date_2))
mvrv = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMVRVCur", date_1, date_2))

df = mcap.merge(realcap, on='date', how='left').merge(mvrv, on='date', how='left')
df.columns = ['date', 'mcap', 'realcap', 'mvrv']

# calc metrics

period = 28

df['MrktGradient'] = ((df['mcap'] - df['mcap'].shift(periods=period, axis=0)) / period)
df['RealGradient'] = ((df['realcap'] - df['realcap'].shift(periods=period, axis=0)) / period)

df['DeltaGradient'] = df['MrktGradient'] - df['RealGradient']

print(df)

#plot
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
line1 = ax1.plot(df['date'], df['DeltaGradient'], color='cyan')
""" line2 = ax1.plot(df['date'], df['MrktGradient'], color = 'cyan', linestyle=':')
line3 = ax1.plot(df['date'], df['RealGradient'], color= 'lime', linestyle=':') """
ax1.set_title("Market Cap vs Realized Cap", fontsize=20, fontweight='bold', color='w')
ax1.fill_between(df['date'], df['DeltaGradient'], where=df['DeltaGradient'] > 0, color='cyan', alpha=0.4)
ax1.fill_between(df['date'], df['DeltaGradient'], where=df['DeltaGradient'] < 0, color='lime', alpha=0.4)
ax1.set_ylabel('Gradient', fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.grid()
ax1.tick_params(color='w', labelcolor='w')
ax1.legend(loc='upper right')
ax1.set_ylim(df['DeltaGradient'].min(), df['DeltaGradient'].max()*1.5)
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = ax1.twinx()
line4 = ax2.plot(df['date'], df['mcap'], color='w')
line5 = ax2.plot(df['date'], df['realcap'], color='r')
ax2.set_ylabel('Network Value', fontsize=20, fontweight='bold', color='w')
ax2.set_yscale('log')
ax2.tick_params(color='w', labelcolor='w')
ax2.legend(loc='upper left')
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax3 = plt.subplot(2,1,2)
ax3.plot(df['date'], df['mvrv'], color='aqua')
ax3.set_title("MVRV Ratio", fontsize=20, fontweight='bold', color='w')
ax3.set_facecolor('black')
ax3.set_ylabel('Ratio Value', fontsize=20, fontweight='bold', color='w')
ax3.set_yscale('log')
ax3.tick_params(color='w', labelcolor='w')
ax3.legend(loc='upper right')
ax3.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
ax3.grid()
ax3.axhspan(0.95, 1.05, color='lime', alpha=0.3)

plt.show()