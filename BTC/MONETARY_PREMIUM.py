import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#fetch desired data
date_1 = "2011-01-01"
date_2 = "2020-04-25"
isstot = cm.get_asset_data_for_time_range(asset, "IssTotUSD", date_1, date_2)
mkt = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2)
# clean CM data
isstot_clean = cm_data_converter.cm_data_convert(isstot)
mkt_clean = cm_data_converter.cm_data_convert(mkt)
# convert to pandas
df = pd.DataFrame(isstot_clean)
df_1 = pd.DataFrame(mkt_clean)
# calc cumulative sum of block rewards
cum_blk_rew = df.cumsum()
# calc monetary premium lines
two_prem = cum_blk_rew*2
four_prem = cum_blk_rew*4
eight_prem = cum_blk_rew*8
sixteen_prem = cum_blk_rew*16
threetwo_prem = cum_blk_rew*32
sixfour_prem = cum_blk_rew*64
#add monetary premium lines to main block rewards dataframe
df_1['Cumulative Block Rewards'] = cum_blk_rew
df_1['Dos'] = two_prem
df_1['Cuatro'] = four_prem
df_1['Ocho'] = eight_prem
df_1['Dieciseis'] = sixteen_prem
df_1['treintados'] = threetwo_prem
df_1['seiscuatro'] = sixfour_prem
print(df_1)
# plot the data

plt.plot(df_1)
plt.title("Market Cap versus Monetary Premiums")
plt.legend((df_1['Cumulative Block Rewards']), ('Block rewards'))
plt.yscale('log')
plt.show()