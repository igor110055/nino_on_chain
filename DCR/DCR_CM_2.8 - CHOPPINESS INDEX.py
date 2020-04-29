import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter
from operator import truediv

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-08-14"
date_2 = "2020-04-28"
oc_flow = cm.get_asset_data_for_time_range(asset, "TxTfrValAdjNtv", date_1, date_2)
flow_clean = cm_data_converter.cm_data_convert(oc_flow)
#print(flow_clean)

mcap = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2)
mcap_clean = cm_data_converter.cm_data_convert(mcap)

# Convert Transactional data to Pandas Dataframe

df_flow = pd.DataFrame(flow_clean)
#df_flow.head()

# Calculate moving sum of coins moved
rolling_flow_28 = df_flow.rolling(window=28).sum()
rolling_flow_56 = df_flow.rolling(window=56).sum()

chop_flow = rolling_flow_28 / rolling_flow_56

# Compare the 28 day and 56 day separately, versus market cap

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(chop_flow)
plt.title("Choppiness")

plt.subplot(2, 1, 2)
plt.plot(mcap_clean)
plt.title("Market Cap")
plt.yscale('log')
plt.show()
