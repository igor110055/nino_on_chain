import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for BTC.
asset = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#fetch desired data
date_1 = "2016-01-01"
date_2 = "2020-05-27"
block = cm.get_asset_data_for_time_range(asset, "BlkCnt", date_1, date_2)
price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)
# clean CM data
block_clean = cm_data_converter.cm_data_convert(block)
price_clean = cm_data_converter.cm_data_convert(price)

# CLEAN DATES

date = cm_data_converter.cm_date_format(price)

# convert to pandas
df = pd.DataFrame(block_clean)
df_1 = pd.DataFrame(price_clean)
# calculate block times in seconds
dia_seconds = 86400
blk_time = dia_seconds / df
#print(blk_time)
#calculate average block time
avg_blk = blk_time.rolling(window=14).mean()
spread_blk = avg_blk - 600

avg_blk1 = blk_time.rolling(window=70).mean()
spread_blk1 = avg_blk1 - 600
# merge price and blk time into a dataset, then send to excel
blk_time['Price'] = df_1
blk_time['Avg'] = avg_blk
blk_time['Spread'] = spread_blk
blk_time['Spread1'] = spread_blk1
blk_time['date'] = date

blk_time['date'] = pd.to_datetime(blk_time['date'], utc=True)

print(blk_time)
""" blk_time.to_excel('btc_blk_times.xlsx') """

#plot blk time versus price
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(blk_time['date'], blk_time['Spread'], label='14 Day Avg Block Time - Target Block Time')
plt.plot(blk_time['date'], blk_time['Spread1'], label='70 Day Avg Block Time - Target Block Time')
plt.title("Block Time")
plt.axhline(0, color='r', linestyle=':')
plt.axhline(50, color='r', linestyle=':')
plt.axhline(-50, color='r', linestyle=':')
""" plt.axhspan(-50, -100, color='g', alpha=0.25)
plt.axhspan(0, 50, color='g', alpha=0.25) """
plt.fill_between(blk_time['date'], blk_time['Spread1'], blk_time['Spread'], where=blk_time['Spread'] > blk_time['Spread1'], facecolor='blue', alpha=0.25)
plt.fill_between(blk_time['date'], blk_time['Spread1'], blk_time['Spread'], where=blk_time['Spread'] < blk_time['Spread1'], facecolor='red', alpha=0.25)
plt.legend()
plt.grid()

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(blk_time['date'], df_1)
plt.title("Price")
plt.yscale('log')
plt.grid()
plt.show()