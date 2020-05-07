import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics.
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#fetch desired data
date_1 = "2016-05-17"
date_2 = "2020-05-06"
diff = cm.get_asset_data_for_time_range(asset, "DiffMean", date_1, date_2)
mkt = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2)
# clean CM data
diff_clean = cm_data_converter.cm_data_convert(diff)
mkt_clean = cm_data_converter.cm_data_convert(mkt)
# convert to pandas
df = pd.DataFrame(diff_clean)
df_1 = pd.DataFrame(mkt_clean)

# calc 200, 128, 90, 60, 40, 25, 14, 9 day ribbons
ribbon_200 = df.rolling(window=200).mean()
ribbon_128 = df.rolling(window=128).mean()
ribbon_90 = df.rolling(window=90).mean()
ribbon_60 = df.rolling(window=60).mean()
ribbon_40 = df.rolling(window=40).mean()
ribbon_25 = df.rolling(window=25).mean()
ribbon_14 = df.rolling(window=14).mean()
ribbon_9 = df.rolling(window=9).mean()

#add ribbons to one dataframe
diff_ribbons = pd.concat([ribbon_200, ribbon_128, ribbon_90, ribbon_60, ribbon_40, ribbon_25, ribbon_14, ribbon_9], axis=1, sort=False)

# ratio calc
ratio = ribbon_9 / ribbon_90

# plot the data
#plot
plt.figure()
ax1 = plt.subplot(3, 1, 1)
plt.plot(ribbon_200, label='200')
plt.plot(ribbon_128, label='128')
plt.plot(ribbon_90, label='90')
plt.plot(ribbon_60, label='60')
plt.plot(ribbon_40, label='40')
plt.plot(ribbon_25, label='25')
plt.plot(ribbon_14, label='14')
plt.plot(ribbon_9, label='9')
plt.yscale('log')
plt.legend()
plt.title("Difficulty Ribbons")

plt.subplot(3, 1, 2, sharex=ax1)
plt.plot(ratio)
plt.title("Ribbon 9 / Ribbon 90 Ratio")
plt.yscale('log')

plt.subplot(3,1,3, sharex=ax1) 
plt.plot(df_1)
plt.title("DCRUSD Market Cap")
plt.yscale('log')
plt.show()