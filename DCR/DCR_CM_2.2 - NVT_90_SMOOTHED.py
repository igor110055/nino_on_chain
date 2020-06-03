# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "dcr"
asset1 = "btc"
date1 = "2016-02-08"
date2 = "2020-05-27"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

dcrbtc = cm.get_asset_data_for_time_range(asset, "PriceBTC", date1, date2)
dcrnvt = cm.get_asset_data_for_time_range(asset, "NVTAdj90", date1, date2)
btcnvt = cm.get_asset_data_for_time_range(asset1, "NVTAdj90", date1, date2)

dcrbtc = cmdc.combo_convert(dcrbtc)
dcrnvt = cmdc.combo_convert(dcrnvt)
btcnvt = cmdc.combo_convert(btcnvt)

df = dcrbtc.merge(dcrnvt, on='date', how='left').merge(btcnvt, on='date', how='left')
df.columns = ['date', 'dcrbtc', 'dcrnvt', 'btcnvt']

df['rel_nvt'] = df['dcrnvt'] / df['btcnvt']
print(df)

plt.plot(df['date'], df['rel_nvt'])
plt.show()