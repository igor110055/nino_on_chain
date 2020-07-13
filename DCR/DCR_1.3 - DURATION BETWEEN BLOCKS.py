# COINMETRICS
import coinmetrics
import cm_data_converter as cmdc

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")
import matplotlib.ticker as ticker

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# Pull data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-07-13"

price = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)

# Clean CM data

cm_df = cmdc.cm_data_convert(price)
cm_df1 = cmdc.cm_date_format(price)

cm_df['date'] = cm_df1
cm_df['date'] = pd.to_datetime(cm_df['date'], utc=True)


#   TICKET DATA
duration = dcrdata.chart("duration-btw-blocks")
print(duration.keys())
print(duration['axis'])
duration_data = duration['duration']
duration_time = duration['t']

# convert to pandas
df = pd.DataFrame(duration_data)

# convert unix to date format and pandas df 
df_1 = pd.to_datetime(duration_time, unit='s', utc=True)

# get average
df_avg63 = df.rolling(window=63).mean()
new_avg = df_avg63 - (300)
df_avg21 = df.rolling(window=21).mean()
new_avg1 = df_avg21 - (300)

# add time to dataframe and print to check that it worked
new_avg['date'] = df_1
new_avg['Raw'] = df

new_avg1['date'] = df_1

# send to excel 
#df.to_excel('duration.xlsx', sheet_name='data')

# Merge CM and dcrdata

comb_df = new_avg.merge(cm_df, on='date', how='left').merge(new_avg1, on='date', how='left')

comb_df.columns = ['Mining Pulse', 'date', 'Block Times', 'DCRBTC', 'Mini Mining Pulse']

print(comb_df)

# plot
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(comb_df['date'], comb_df['Mining Pulse'], color='aqua', alpha=0.7)
ax1.set_facecolor('black')
ax1.set_ylabel('Seconds Faster / Slower than Target', fontsize=12, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.axhline(2, linestyle='dashed', color='lime')
ax1.axhline(-2, linestyle='dashed', color='lime')
ax1.fill_between(comb_df['date'], comb_df['Mining Pulse'], where=comb_df['Mining Pulse'] > 0, facecolor='aqua', alpha=0.4)
ax1.fill_between(comb_df['date'], comb_df['Mining Pulse'], where=comb_df['Mining Pulse'] < 0, facecolor='red', alpha=0.4)
ax1.set_title("Mining Pulse (63 Days) vs DCRBTC Price", fontsize=20, fontweight='bold', color='w')
ax1.grid()

ax2 = ax1.twinx()
ax2.plot(comb_df['date'], comb_df['DCRBTC'], color='w')
ax2.set_ylabel('DCRBTC', fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax3 = plt.subplot(2,1,2, sharex=ax1)
ax3.plot(comb_df['date'], comb_df['Mini Mining Pulse'], color='aqua', alpha=0.7)
ax3.set_facecolor('black')
ax3.set_ylabel('Seconds Faster / Slower than Target', fontsize=12, fontweight='bold', color='w')
ax3.tick_params(color='w', labelcolor='w')
ax3.axhline(5, linestyle='dashed', color='lime')
ax3.axhline(-5, linestyle='dashed', color='lime')
ax3.fill_between(comb_df['date'], comb_df['Mini Mining Pulse'], where=comb_df['Mini Mining Pulse'] > 0, facecolor='aqua', alpha=0.4)
ax3.fill_between(comb_df['date'], comb_df['Mini Mining Pulse'], where=comb_df['Mini Mining Pulse'] < 0, facecolor='red', alpha=0.4)
ax3.set_title("Mini Mining Pulse (21 Days) vs DCRBTC Price", fontsize=20, fontweight='bold', color='w')
ax3.grid()

ax4 = ax3.twinx()
ax4.plot(comb_df['date'], comb_df['DCRBTC'], color='w')
ax4.set_ylabel('DCRBTC', fontsize=20, fontweight='bold', color='w')
ax4.tick_params(color='w', labelcolor='w')
ax4.set_yscale('log')
ax4.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

plt.show()