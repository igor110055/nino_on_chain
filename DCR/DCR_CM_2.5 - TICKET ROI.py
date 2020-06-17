import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib as mpl

# Add early price data

filename = 'DCR/DCR_data.xlsx'
df_early = pd.read_excel(filename)
early = df_early[['date', 'PriceUSD', 'PriceBTC']].copy()
early['date'] = pd.to_datetime(early['date'], utc=True)

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics.
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

#fetch and format desired data
date_1 = "2011-01-01"
date_2 = "2020-06-11"

supply = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "SplyCur", date_1, date_2))
dcrusd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
dcrbtc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))

df = supply.merge(dcrusd, on='date', how='left').merge(dcrbtc, on='date', how='left')
df.columns = ['date', 'supply', 'dcrusd', 'dcrbtc']

df = df.merge(early, on='date', how='left')
df = df.fillna(0)

df['dcrusd'].mask(df['dcrusd'] == 0, df['PriceUSD'], inplace=True)
df['dcrbtc'].mask(df['dcrbtc'] == 0, df['PriceBTC'], inplace=True)

df = df.drop(columns=['PriceUSD', 'PriceBTC'])

plt.plot(df['date'], df['dcrusd'])
plt.show()

