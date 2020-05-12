import coinmetrics
import matplotlib.pyplot as plt
import pandas as pd
import cm_data_converter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#fetch desired data
date_1 = "2016-11-01"
date_2 = "2020-05-09"
tx = cm.get_asset_data_for_time_range(asset, "TxTfrValAdjNtv", date_1, date_2)
price = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)
# clean CM data
tx_clean = cm_data_converter.cm_data_convert(tx)
price_clean = cm_data_converter.cm_data_convert(price)
# convert to pandas
df = pd.DataFrame(tx_clean)
df_1 = pd.DataFrame(price_clean)
# CALC AVGS AND RATIO
avg28 = df.rolling(window=28).sum()
avg56 = df.rolling(window=56).sum()
ratio = avg28 / avg56
# plot
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(avg28)
plt.title("TX FLOWS RATIO")

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df_1)
plt.title("ALTBTC PRICE")
plt.yscale('log')
plt.show()