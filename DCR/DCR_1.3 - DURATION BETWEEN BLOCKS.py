# COINMETRICS
import coinmetrics
import cm_data_converter as cmdc

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# Pull data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-06-02"

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
fig = plt.figure()
fig.patch.set_facecolor('#E0E0E0')
fig.patch.set_alpha(0.7)

ax1 = plt.subplot(3,1,1)
plt.plot(comb_df['date'], comb_df['Mining Pulse'])
plt.axhspan(2, 4, color='g', alpha=0.25)
plt.axhspan(-2, -4, color='g', alpha=0.25)
plt.axhline(0, linestyle=':', color='r')
plt.fill_between(comb_df['date'], comb_df['Mining Pulse'], where=comb_df['Mining Pulse'] > 0, facecolor='blue', alpha=0.25)
plt.fill_between(comb_df['date'], comb_df['Mining Pulse'], where=comb_df['Mining Pulse'] < 0, facecolor='red', alpha=0.25)
#plt.plot(new_avg1)
plt.title("Mining Pulse (Unit = Seconds)")
plt.grid()

plt.subplot(3,1,2, sharex=ax1)
plt.plot(comb_df['date'], comb_df['DCRBTC'])
plt.yscale('log')
plt.grid()

plt.subplot(3,1,3, sharex=ax1)
plt.plot(comb_df['date'], comb_df['Mini Mining Pulse'])
plt.fill_between(comb_df['date'], comb_df['Mini Mining Pulse'], where=comb_df['Mini Mining Pulse'] > 0, facecolor='blue', alpha=0.25)
plt.fill_between(comb_df['date'], comb_df['Mini Mining Pulse'], where=comb_df['Mini Mining Pulse'] < 0, facecolor='red', alpha=0.25)
plt.axhspan(5, 10, color='g', alpha=0.25)
plt.axhspan(-5, -10, color='g', alpha=0.25)
plt.grid()

plt.show()