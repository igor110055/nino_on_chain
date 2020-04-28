import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for alts.
asset = "eth"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#fetch desired data
date_1 = "2011-01-01"
date_2 = "2020-04-25"
block = cm.get_asset_data_for_time_range(asset, "BlkCnt", date_1, date_2)
price = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)
#convert to pandas
df = pd.DataFrame(block)
df_1 = pd.DataFrame(price)
# print to check
print(df)