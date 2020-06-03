import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for alts.
asset = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#fetch desired data
date_1 = "2011-01-01"
date_2 = "2020-06-01"
block = cm.get_asset_data_for_time_range(asset, "BlkCnt", date_1, date_2)
price = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)
# clean CM data
block_clean = cm_data_converter.cm_data_convert(block)
price_clean = cm_data_converter.cm_data_convert(price)
# convert to pandas
df = pd.DataFrame(block_clean)
df_1 = pd.DataFrame(price_clean)
# calculate block times in seconds
dia_seconds = 86400
blk_time = dia_seconds / df
print(blk_time)
# merge price and blk time into a dataset, then send to excel
blk_time['Price'] = df_1

#blk_time.to_excel('bsv_blk_times.xlsx')
#plot blk time versus price
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(blk_time[0])
plt.yscale('log')
plt.title("Block Time")

plt.subplot(2, 1, 2)
plt.plot(df_1)
plt.title("Price")
plt.yscale('log')
plt.show()