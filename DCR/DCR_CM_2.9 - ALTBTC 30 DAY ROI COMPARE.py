# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc


# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# Pull data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-08-14"
date_2 = "2020-05-11"

price = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)

# Clean data

df = cmdc.cm_data_convert(price)
df_1 = cmdc.cm_date_format(price)

# Calc 30-day DCRBTC ROI

df_2 = df.pct_change(periods=30)

# Merge datasets

df_1['DCRBTC'] = df
df_1['ROI'] = df_2

# Print merged data

print(df_1)

# Plot dcrbtc price and roi

#plot
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(df_1[0], df_1['ROI'])
plt.fill_between(df_1[0], df_1['ROI'], color='r')
plt.title("30-Day DCRBTC ROI")
plt.grid()
plt.axhspan(-.25, .45, color='g', alpha=0.25)
plt.ylim(-0.7, 1.5)

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df_1[0], df_1['DCRBTC'])
plt.title("DCRBTC")
plt.yscale('log')
plt.grid()
plt.show()

