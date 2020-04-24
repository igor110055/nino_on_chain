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
asset = "link"
asset_1 = "btc"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-08-14"
date_2 = "2020-04-20"
roi = cm.get_asset_data_for_time_range(asset, "ROI30d", date_1, date_2)
mcap = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)
btc_roi = cm.get_asset_data_for_time_range(asset_1, "ROI30d", date_1, date_2)

roi_clean = cm_data_converter.cm_data_convert(roi)
mcap_clean = cm_data_converter.cm_data_convert(mcap)
btc_roi_clean = cm_data_converter.cm_data_convert(btc_roi)
# Convert to pandas dataframe

df = pd.DataFrame(roi_clean)
df_1 = pd.DataFrame(mcap_clean)
df_2 = pd.DataFrame(btc_roi_clean)

# Calculate altbtc roi compare

altbtc_roi = df / df_2
altbtc_28avg = altbtc_roi.rolling(window=28).mean()
# plot

plt.plot(altbtc_28avg)
plt.show()


