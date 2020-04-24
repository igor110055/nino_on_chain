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
hash = cm.get_asset_data_for_time_range(asset, "HashRate", date_1, date_2)
price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)
# clean CM data
hash_clean = cm_data_converter.cm_data_convert(hash)
price_clean = cm_data_converter.cm_data_convert(price)
# convert to pandas
df = pd.DataFrame(hash_clean)
df_1 = pd.DataFrame(price_clean)
#compute 200 MA
MA_180 = df.rolling(window=180).mean()
#compute ratio
ratio = df / MA_180
print(ratio)
#plot ratio versus price
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(ratio)
plt.title("Current Hashrate / 180 HR MA Ratio")

plt.subplot(2, 1, 2)
plt.plot(df_1)
plt.title("Price")
plt.yscale('log')
plt.show()