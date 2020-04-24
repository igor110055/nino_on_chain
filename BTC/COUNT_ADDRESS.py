import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#fetch desired data
date_1 = "2011-01-01"
date_2 = "2020-04-22"
addr = cm.get_asset_data_for_time_range(asset, "AdrActCnt", date_1, date_2)
price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)
# clean CM data
addr_clean = cm_data_converter.cm_data_convert(addr)
price_clean = cm_data_converter.cm_data_convert(price)
# convert to pandas
df = pd.DataFrame(addr_clean)
df_1 = pd.DataFrame(price_clean)
# calc address avg & ratio
addr_avg = df.rolling(window=90).mean()
ratio = df / addr_avg
#plot versus price
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(ratio)
plt.title("Address Density")

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df_1)
plt.title("Price")
plt.yscale('log')
plt.show()