# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# Usage Examples ############################################################

# List the assets Coin Metrics has data for.
supported_assets = cm.get_supported_assets()
print("supported assets:\n", supported_assets)

# List all available metrics for DCR.
asset = "dcr"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

nvt90 = cm.get_asset_data_for_time_range(asset, "NVTAdj90", "2016-02-08", "2020-04-20")
#print(nvt90)

#print(nvt90.keys())
nvt90_list_values = []
nvt90_list = nvt90['series']
#print(nvt90_list)
for nvt_dict in nvt90_list:
    nvt90_list_values.append(nvt_dict['values'])

#print(nvt90_list_values)
nvt90_str_values = []
for list_value in nvt90_list_values:
    nvt90_str_values.append(list_value[0])

#print(nvt90_str_values)

float_nvt90 = list(map(float, nvt90_str_values))
#print(float_nvt90)

plt.title("NVT RATIO 90-DAY SMOOTHED", fontsize=20)
plt.ylabel("RATIO", fontsize=14)

plt.plot(float_nvt90, color='green')
plt.show()






