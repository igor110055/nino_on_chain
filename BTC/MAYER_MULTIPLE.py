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
date_1 = "2013-01-01"
date_2 = "2020-04-22"
price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)
# clean CM data
price_clean = cm_data_converter.cm_data_convert(price)
# convert to pandas
df = pd.DataFrame(price_clean)
#compute 200 MA
MA_200 = df.rolling(window=200).mean()
#Calc mayer multiple
Mayer_Mult = df / MA_200
print(Mayer_Mult)
## 0.6 is a good place to buy for Mayer Multiple - calculate 0.6*200MA and add to plot
hard_buy = 0.6 * MA_200

## Add hard buy to price dataset
df['Hard Buy'] = hard_buy

#plot price vs mayer
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(Mayer_Mult)
plt.title("Mayer Multiple")

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df)
plt.title("USD Price")
plt.yscale('log')
plt.show()
