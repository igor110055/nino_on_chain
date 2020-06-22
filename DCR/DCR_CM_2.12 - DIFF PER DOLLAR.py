# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# PULL DCR CM DATA

asset = "dcr"
date_1 = "2016-08-14"
date_2 = "2020-06-21"

dcr_price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)
dcr_diff = cm.get_asset_data_for_time_range(asset, "DiffMean", date_1, date_2)

dcr_price = cmdc.combo_convert(dcr_price)
dcr_diff = cmdc.combo_convert(dcr_diff)

df = dcr_price.merge(dcr_diff, on='date', how='left')

df.columns = ['date', 'PriceUSD', 'Diff']

# CALC METRICS

df['diffdollar'] = df['Diff'] / df['PriceUSD']
df['avgdd'] = df['diffdollar'].rolling(14).mean()
df['avgdd1'] = df['diffdollar'].rolling(42).mean()
df['surplus'] = df['avgdd'] - df['avgdd1']

# PLOT

plt.figure()
ax1 = plt.subplot(2,1,1)
plt.plot(df['date'], df['surplus'], label='Diff per Dollar Surplus / Deficit')
plt.fill_between(df['date'], df['surplus'], where=df['surplus'] > 0, facecolor='blue', alpha=0.25)
plt.fill_between(df['date'], df['surplus'], where=df['surplus'] < 0, facecolor='red', alpha=0.25)
plt.title("Diff per Dollar Surplus / Deficit")
plt.grid()
plt.legend()

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df['date'], df['PriceUSD'])
plt.yscale('log')
plt.title("DCRBTC")
plt.grid()
plt.show()