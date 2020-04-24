# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "dcr"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

# Get DCR MVRV Data

Date_1 = "2016-08-14"
Date_2 = "2020-04-19"
MVRV_Raw_Data = cm.get_asset_data_for_time_range(asset, "CapMVRVCur", Date_1, Date_2)
#print(MVRV_Raw_Data)
#print(MVRV_Raw_Data['series'])
MVRV_series = MVRV_Raw_Data['series']
MVRV_list = []
MVRV_list_list = []
for mvrv in MVRV_series:
    MVRV_list.append(mvrv['values'])
#print(MVRV_list)
for mvrv_mvrv in MVRV_list:
    MVRV_list_list.append(mvrv_mvrv[0])
#print(MVRV_list_list)

float_MVRV = list(map(float, MVRV_list_list))
#print(float_MVRV)

plt.plot(float_MVRV)
plt.ylabel("Ratio")
plt.title("Decred MVRV Ratio")
plt.show()
