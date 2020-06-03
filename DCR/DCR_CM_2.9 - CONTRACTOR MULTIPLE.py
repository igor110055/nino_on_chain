import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter


# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#Fetch data
date_1 = "2016-08-14"
date_2 = "2020-06-01"
price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)
#clean data
price_clean = cm_data_converter.cm_data_convert(price)
#convert to pandas
df = pd.DataFrame(price_clean)
#calc 30-day avg
MA_30 = df.rolling(window=30).mean()
# ratio calc
ratio = df / MA_30
print(ratio)
#Merge dataframes (for sending to excel)
df['30 MA'] = MA_30
#Send to excel
#df.to_excel('Contractor_Mult.xlsx')
#0.7 is a quality buy zone, build buy zone price and add to price dataframe
hard_buy = 0.7*df['30 MA']

# merge hard buy to price dataframe
df['Hard Buy'] = hard_buy

#plot
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(ratio)
plt.axhspan(0.7, 1.35, color='g', alpha=0.25)
plt.grid()
plt.title("Contractor Multiple")

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df)
plt.title("DCRUSD")
plt.yscale('log')
plt.grid()
plt.show()
