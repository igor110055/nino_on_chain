import coinmetrics
import cm_data_converter as cmdc

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")
import matplotlib.ticker as ticker
import matplotlib as mpl

# Add csv

filename = 'DCR/treasury.csv'
df = pd.read_csv(filename)

# Format csv

df = df.drop(columns=['tx_hash', 'io_index', 'valid_mainchain', 'tx_type', 'matching_tx_hash'])
df['time_stamp'] = pd.to_datetime(df['time_stamp'], unit='s').dt.strftime('%Y-%m-%d')
df = df.sort_values(by='time_stamp')
df = df.reset_index()

df['value'] = df['direction'] * df['value']   # change values negatives if outflow

df1 = df.groupby('time_stamp')['value'].sum()
df1 = pd.DataFrame(df1)

# CM data
cm = coinmetrics.Community()
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-08-04"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
mcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))

# Merge treasury and CM data

price = price.merge(mcap, on='date', how='left')
price['date'] = price['date'].dt.strftime('%Y-%m-%d')   # convert date to merge
price.columns = ['time_stamp', 'PriceUSD', 'Mcap']
df1 = df1.merge(price, on='time_stamp', how='left')
df1['time_stamp'] = pd.to_datetime(df1['time_stamp']) # change back to datetime for plotting

# Calc Metrics

df1['valueusd'] = df1['value'] * df1['PriceUSD']
df1['monthflow'] = df1['value'].rolling(90).sum()

print(df1)

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
ax1.plot(df1['time_stamp'], df1['monthflow'], color='lime', alpha=0.5)
ax1.set_facecolor('black')
ax1.set_ylabel('Daily Treasury Inflow / Outflow (DCR)', fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_title("Market Cap vs Treasury Flows", fontsize=20, fontweight='bold', color='w')
ax1.fill_between(df1['time_stamp'], df1['monthflow'], where= df1['monthflow'] > 0, facecolor='aqua', alpha=0.4)
ax1.fill_between(df1['time_stamp'], df1['monthflow'], where= df1['monthflow'] < 0, facecolor='red', alpha=0.4)
ax1.grid()
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = ax1.twinx()
ax2.plot(df1['time_stamp'], df1['Mcap'], color='w')
ax2.set_ylabel('Market Cap', fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

plt.show()