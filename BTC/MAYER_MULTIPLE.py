import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "eth"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#fetch desired data
date_1 = "2011-01-01"
date_2 = "2020-08-11"
price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)
# clean CM data
df = cm_data_converter.combo_convert(price)

df.columns = ['date', 'price']

# Calc Metrics

df['MA_200'] = df['price'].rolling(window=200).mean()
df['Mayer_Mult'] = df['price'] / df['MA_200']
df['hard_buy'] = 0.6 * df['MA_200']
df['hard_sell'] = 2.3 * df['MA_200']
df['Mayer_Avg'] = df['Mayer_Mult'].rolling(200).mean()
df['Dynamic_Mayer'] = df['Mayer_Avg'] * df['MA_200']
df['Dynamic_Mult'] = df['Mayer_Mult'] / df['Mayer_Avg']

print(df)

#plot price vs mayer
plt.figure()
ax1 = plt.subplot(2, 1, 1)
""" plt.plot(df['date'], df['Mayer_Mult'])
plt.plot(df['date'], df['Mayer_Avg'], linestyle=':') """
plt.plot(df['date'], df['Dynamic_Mult'])
plt.axhline(1, linestyle=':', color='r')
plt.title("Mayer Multiple")
plt.legend()
plt.grid()

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df['date'], df['price'])
plt.plot(df['date'], df['hard_buy'])
plt.plot(df['date'], df['hard_sell'])
plt.plot(df['date'], df['Dynamic_Mayer'], linestyle=':')
plt.plot(df['date'], df['MA_200'], linestyle=':')
plt.title("USD Price")
plt.yscale('log')
plt.grid()
plt.legend()
plt.show()
