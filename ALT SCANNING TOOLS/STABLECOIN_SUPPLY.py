# THIS CODE WILL HELP KICK OFF WORK ON A NEW MODULE, JUST COPY + PASTE

# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "usdt"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

# List assets & dates

date_1 = "2011-01-01"
date_2 = "2020-05-05"

asset = "btc"
asset1 = "busd"
asset2 = "husd"
asset3 = "tusd"
asset4 = "usdc"
asset5 = "usdt"
asset6 = "usdt_eth"
asset7 = "usdt_trx"

# List the assets Coin Metrics has data for.
supported_assets = cm.get_supported_assets()
print("supported assets:\n", supported_assets)

#fetch desired data

btc = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2)
busd = cm.get_asset_data_for_time_range(asset1, "CapMrktCurUSD", date_1, date_2)
husd = cm.get_asset_data_for_time_range(asset2, "CapMrktCurUSD", date_1, date_2)
tusd = cm.get_asset_data_for_time_range(asset3, "CapMrktCurUSD", date_1, date_2)
usdc = cm.get_asset_data_for_time_range(asset4, "CapMrktCurUSD", date_1, date_2)
usdt = cm.get_asset_data_for_time_range(asset5, "CapMrktCurUSD", date_1, date_2)
usdt_eth = cm.get_asset_data_for_time_range(asset6, "CapMrktCurUSD", date_1, date_2)
usdt_trx = cm.get_asset_data_for_time_range(asset7, "CapMrktCurUSD", date_1, date_2)

# clean CM data for each stablecoin

btc_clean = cmdc.cm_data_convert(btc)
busd_clean = cmdc.cm_data_convert(busd)
husd_clean = cmdc.cm_data_convert(husd)
tusd_clean = cmdc.cm_data_convert(tusd)
usdc_clean = cmdc.cm_data_convert(usdc)
usdt_clean = cmdc.cm_data_convert(usdt)
usdteth_clean = cmdc.cm_data_convert(usdt_eth)
usdttrx_clean = cmdc.cm_data_convert(usdt_trx)

#btc_dates = cmdc.cm_date_format(btc)
#print(btc_dates)

# turn into single dataframe

df = pd.DataFrame(btc_clean)
df1 = pd.DataFrame(busd_clean)
df2 = pd.DataFrame(husd_clean)
df3 = pd.DataFrame(tusd_clean)
df4 = pd.DataFrame(usdc_clean)
df5 = pd.DataFrame(usdt_clean)
df6 = pd.DataFrame(usdteth_clean)
df7 = pd.DataFrame(usdttrx_clean)

stable = pd.concat([df, df1, df2, df3, df4, df5, df6, df7], axis=1, sort=False)

#print(stable)

#stable.to_excel('stablecoins.xlsx')

#plot
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(df5)
plt.title("Stablecoin Market Cap")

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df)
plt.title("DCRUSD")
plt.yscale('log')
plt.show()