# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# PULL DCR & BTC NTV, MVRV, & REALIZED PRICE DATA "2016-08-14"

asset = "dcr"
asset2 = "btc"
date_1 = "2016-08-14"
date_2 = "2020-05-11"

coin_price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)
coin1_price = cm.get_asset_data_for_time_range(asset2, "PriceUSD", date_1, date_2)

dcr_real = cm.get_asset_data_for_time_range(asset, "CapRealUSD", date_1, date_2)
btc_real = cm.get_asset_data_for_time_range(asset2, "CapRealUSD", date_1, date_2)

dcr_nvt = cm.get_asset_data_for_time_range(asset, "NVTAdj90", date_1, date_2)
btc_nvt = cm.get_asset_data_for_time_range(asset2, "NVTAdj90", date_1, date_2)

dcr_mvrv = cm.get_asset_data_for_time_range(asset, "CapMVRVCur", date_1, date_2)
btc_mvrv = cm.get_asset_data_for_time_range(asset2, "CapMVRVCur", date_1, date_2)

# CLEAN DATA USING DATA CONVERTER & CONVERT TO PANDAS

priceclean = pd.DataFrame(cmdc.cm_data_convert(coin_price))
priceclean1 = pd.DataFrame(cmdc.cm_data_convert(coin1_price))

dcrrealclean = pd.DataFrame(cmdc.cm_data_convert(dcr_real))  
btcrealclean = pd.DataFrame(cmdc.cm_data_convert(btc_real)) 

dcrnvtclean = pd.DataFrame(cmdc.cm_data_convert(dcr_nvt)) 
btcnvtclean = pd.DataFrame(cmdc.cm_data_convert(btc_nvt))  

dcrmvrvclean = pd.DataFrame(cmdc.cm_data_convert(dcr_mvrv))  
btcmvrvclean = pd.DataFrame(cmdc.cm_data_convert(btc_mvrv))  

# CALC REALTIVE VALUE RATIOS

rel_real = dcrrealclean / btcrealclean
rel_nvt = dcrnvtclean / btcnvtclean
rel_mvrv = dcrmvrvclean / btcmvrvclean
coin_coin1 = priceclean / priceclean1

# CALC RELATIVE VALUE PRICES

rel_nvt_price = coin_coin1 / rel_nvt
rel_mvrv_price = coin_coin1 / rel_mvrv
mid_point = 0.5 * (rel_real + rel_mvrv_price)

# MERGE DATASETS
df = pd.concat([priceclean, priceclean1, rel_real, rel_nvt_price, rel_mvrv_price], axis=1, sort=False)

# SEND TO EXCEL
#df.to_excel('Relative Value Prices.xlsx')

# PLOT VALUES

plt.plot(coin_coin1, label='DCRBTC Market Traded Price')
plt.plot(rel_real, label='DCR Realized Price / BTC Realized Price', linestyle=':')
plt.plot(rel_mvrv_price, label='Relative MVRV Price', linestyle=':')
plt.plot(mid_point, label='Mid-Point', linestyle=':')
plt.ylabel("DCRBTC PRICES")
plt.yscale('log')
plt.legend()
plt.title("Relative Value Prices")
plt.show()