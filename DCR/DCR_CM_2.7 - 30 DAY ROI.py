# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter


# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-07-01"
date_2 = "2020-05-06"
roi = cm.get_asset_data_for_time_range(asset, "ROI30d", date_1, date_2)
mcap = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2)

roi_clean = cm_data_converter.cm_data_convert(roi)
mcap_clean = cm_data_converter.cm_data_convert(mcap)

print(roi_clean)
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(roi_clean, linestyle=':')
plt.title("30 Day ROI")

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(mcap_clean)
plt.title("Market Cap")
plt.yscale('log')
plt.show()