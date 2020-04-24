# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List the assets Coin Metrics has data for.
supported_assets = cm.get_supported_assets()
print("supported assets:\n", supported_assets)

# List all available metrics for DCR.
asset = "dcr"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

# retrieve the historical data for realized cap

real_cap = cm.get_real_cap("dcr", "2016-05-17", "2020-04-17")
#print(real_cap)

# pull market cap and prepare the data for plotting

Market_Cap_Hist = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", "2016-02-08", "2020-04-17")
print(Market_Cap_Hist)

cap_x_val = []
cap_y_val = []
cap_y_val_final = []

#print(Market_Cap_Hist.keys())

cap_series = Market_Cap_Hist['series']
# print(cap_series)

for date in cap_series:
    cap_x_val.append(date['time'])

for real_value in cap_series:
    cap_y_val.append(real_value['values'])

for value in cap_y_val:
    y_pop = value.pop()
    cap_y_val_final.append(y_pop)

plt.plot
cap_y_val_final = list(map(float, cap_y_val_final))
print(cap_y_val_final)

# pull dates and values out of the realized cap history, put them into axes, changes values from strings to floats (prints in this section are just to check that i did shit correctly)

real_x_val = []
real_y_val = []
real_y_val_final = []

#print(real_cap.keys())

real_cap_series = real_cap['series']
# print(real_cap_series)

for date in real_cap_series:
    real_x_val.append(date['time'])

for real_value in real_cap_series:
    real_y_val.append(real_value['values'])

for value in real_y_val:
    y_pop = value.pop()
    real_y_val_final.append(y_pop)

real_y_val_final = list(map(float, real_y_val_final))
#print(real_y_val_final)

# convert dates from strings into datetime objects


# plot the realized cap

plt.plot(real_y_val_final)
plt.plot(cap_y_val_final)
plt.yscale('log')
plt.show()

