# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
from operator import truediv

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# DECRED REALIZED CAP DATA

asset = "dcr"
date_1 = "2016-08-14"
date_2 = "2020-04-20"

dcr_real = cm.get_asset_data_for_time_range(asset, "CapRealUSD", date_1, date_2)
#print(nvt90)

#print(nvt90.keys())
dcrreal_list_values = []
dcrreal_list = dcr_real['series']
#print(nvt90_list)
for real_dict in dcrreal_list:
    dcrreal_list_values.append(real_dict['values'])

#print(nvt90_list_values)
dcrreal_str_values = []
for list_value in dcrreal_list_values:
    dcrreal_str_values.append(list_value[0])

#print(nvt90_str_values)

float_dcrreal = list(map(float, dcrreal_str_values))
#print(float_nvt90)

# BTC REALIZED CAP DATA

asset_2 = "btc"

btc_real = cm.get_asset_data_for_time_range(asset_2, "CapRealUSD", date_1, date_2)
#print(btc_nvt90)

#print(btc_nvt90.keys())
btc_real_list_values = []
btc_real_list = btc_real['series']
#print(btc_nvt90_list)
for btc_real_dict in btc_real_list:
    btc_real_list_values.append(btc_real_dict['values'])

#print(btc_nvt90_list_values)
btc_real_str_values = []
for btc_list_value in btc_real_list_values:
    btc_real_str_values.append(btc_list_value[0])

#print(nvt90_str_values)

btc_float_real = list(map(float, btc_real_str_values))
#print(btc_float_nvt90)

#relative_value = [i / j for i, j in zip(float_nvt90, btc_float_nvt90)]
relative_value = list(map(truediv, float_dcrreal, btc_float_real))

print(relative_value)
plt.plot(relative_value, color='red')
plt.yscale('log')
plt.title("ON-CHAIN DCRBTC PRICE", fontsize=20)
plt.ylabel("RATIO", fontsize=14)
plt.show()