# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
from operator import truediv

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# Get DCR MVRV Data
asset = "dcr"
Date_1 = "2016-08-14"
Date_2 = "2020-04-17"
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

# Get BTC MVRV Data
asset_1 = "btc"
BTC_MVRV_Raw_Data = cm.get_asset_data_for_time_range(asset_1, "CapMVRVCur", Date_1, Date_2)

BTC_MVRV_series = BTC_MVRV_Raw_Data['series']
BTC_MVRV_list = []
BTC_MVRV_list_list = []
for mvrv in BTC_MVRV_series:
    BTC_MVRV_list.append(mvrv['values'])

for mvrv_mvrv in BTC_MVRV_list:
    BTC_MVRV_list_list.append(mvrv_mvrv[0])

BTC_float_MVRV = list(map(float, BTC_MVRV_list_list))
#print(BTC_float_MVRV)

# Calculative Relative Value

#relative_value = [i / j for i, j in zip(float_nvt90, btc_float_nvt90)]
relative_value = list(map(truediv, float_MVRV, BTC_float_MVRV))

plt.plot(relative_value)
plt.ylabel("Ratio")
plt.title("Relative MVRV Ratio")
plt.show()