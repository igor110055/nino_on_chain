import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics.
asset = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#fetch desired data
date_1 = "2011-01-01"
date_2 = "2020-05-22"
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

plt.plot(df_1[0], label='Market Cap')
plt.plot(df_1['Cumulative Block Rewards'], label='Block Rewards Sum')
plt.plot(df_1['Dos'], label='2x')
plt.plot(df_1['Cuatro'], label='4x')
plt.plot(df_1['Ocho'], label='8x')
plt.plot(df_1['Dieciseis'], label='16x')
plt.plot(df_1['treintados'], label='32x')
plt.plot(df_1['seiscuatro'], label='64x')
plt.legend()
plt.title("Market Cap versus Monetary Premiums")
plt.yscale('log')
plt.show()