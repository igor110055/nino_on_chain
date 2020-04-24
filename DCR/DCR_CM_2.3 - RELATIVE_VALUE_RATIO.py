# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
from operator import truediv

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# DECRED NVT90 DATA

asset = "dcr"
date_1 = "2016-08-14"
date_2 = "2020-04-18"

nvt90 = cm.get_asset_data_for_time_range(asset, "NVTAdj90", date_1, date_2)
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

# BTC NVT90 DATA

asset_2 = "btc"

btc_nvt90 = cm.get_asset_data_for_time_range(asset_2, "NVTAdj90", date_1, date_2)
#print(btc_nvt90)

#print(btc_nvt90.keys())
btc_nvt90_list_values = []
btc_nvt90_list = btc_nvt90['series']
#print(btc_nvt90_list)
for btc_nvt_dict in btc_nvt90_list:
    btc_nvt90_list_values.append(btc_nvt_dict['values'])

#print(btc_nvt90_list_values)
btc_nvt90_str_values = []
for btc_list_value in btc_nvt90_list_values:
    btc_nvt90_str_values.append(btc_list_value[0])

#print(nvt90_str_values)

btc_float_nvt90 = list(map(float, btc_nvt90_str_values))
#print(btc_float_nvt90)

#relative_value = [i / j for i, j in zip(float_nvt90, btc_float_nvt90)]
relative_value = list(map(truediv, float_nvt90, btc_float_nvt90))

print(relative_value)
plt.plot(relative_value, color='red')
plt.yscale('log')
plt.title("RELATIVE VALUE RATIO", fontsize=20)
plt.ylabel("RATIO", fontsize=14)
plt.show()