import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics.
asset = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

#fetch desired data
date_1 = "2010-01-01"
date_2 = "2020-06-04"

mcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))
subsidy = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "IssTotUSD", date_1, date_2))
fees = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "FeeTotUSD", date_1, date_2))
diff = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "DiffMean", date_1, date_2))
price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
blk = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "BlkCnt", date_1, date_2))

df = mcap.merge(subsidy, on='date', how='left').merge(fees, on='date', how='left').merge(diff, on='date', how='left').merge(price, on='date', how='left').merge(blk, on='date', how='left')
df.columns = ['date', 'mcap', 'subsidy', 'fees', 'diff', 'price', 'blkcount']

# Calc Metrics

df['rewardstot'] = df['subsidy'] + df['fees']
df['rewardblock'] = df['rewardstot'] / df['blkcount']
df['feeblock'] = df['fees'] / df['blkcount']
df['diff_200'] = df['diff'].rolling(200).mean()
df['diffratio'] = df['diff'] / df['diff_200']
df['365_iss'] = df['subsidy'].rolling(365).mean()
df['feeshare'] = df['fees'] / df['rewardstot']

df['miningcost'] = df['rewardstot'] * (1 / df['diffratio'])
df['miningprofit'] = df['rewardstot'] - df['miningcost']
df['miningprofitcoins'] = df['miningprofit'] / df['price']
df['puell_mult'] = df['subsidy'] / df['365_iss']
df['puelltop'] = df['mcap'].rolling(365).mean() * 6
df['puellbot'] = df['mcap'].rolling(365).mean() * 0.4
df['blockpriceratio'] = df['rewardblock'] / df['price']
df['feeratio'] = df['feeblock'] / df['price']

print(df)

# PLOT

fig = plt.figure()
fig.patch.set_facecolor('#E0E0E0')
fig.patch.set_alpha(0.7)

ax1 = plt.subplot(2,1,1)
plt.plot(df['date'], df['feeratio'])

""" plt.fill_between(df['date'], df['miningprofitcoins'], where=df['miningprofitcoins'] > 0, facecolor='blue', alpha=0.25)
plt.fill_between(df['date'], df['miningprofitcoins'], where=df['miningprofitcoins'] < 0, facecolor='red', alpha=0.25) """
plt.title("Mining Industry Revenue / Cost / Profit")
plt.yscale('log')
plt.legend()
plt.grid()

plt.subplot(2,1,2, sharex=ax1)
plt.plot(df['date'], df['rewardblock'])
plt.plot(df['date'], df['price'])

plt.yscale('log')
plt.grid()

plt.show()