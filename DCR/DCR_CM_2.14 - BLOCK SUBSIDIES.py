import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics.
asset = "dcr"
asset1 = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

# Add early price data

filename = 'DCR/DCR_data.xlsx'
df_early = pd.read_excel(filename)
early = df_early[['date', 'PriceUSD', 'PriceBTC', 'CapMrktCurUSD']].copy()
early['date'] = pd.to_datetime(early['date'], utc=True)
print(early)

#fetch desired data
date_1 = "2011-01-01"
date_2 = "2020-06-07"

supply = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "SplyCur", date_1, date_2))
dcrusd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
dcrbtc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))
btcusd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "PriceUSD", date_1, date_2))
dcrmarketcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))

df = supply.merge(dcrusd, on='date', how='left').merge(dcrbtc, on='date', how='left').merge(btcusd, on='date', how='left').merge(dcrmarketcap, on='date', how='left')
df.columns = ['date', 'supply', 'dcrusd', 'dcrbtc', 'btcusd', 'dcrmarketcap']

df = df.merge(early, on='date', how='left')
df = df.fillna(0)

df['dcrusd'].mask(df['dcrusd'] == 0, df['PriceUSD'], inplace=True)
df['dcrbtc'].mask(df['dcrbtc'] == 0, df['PriceBTC'], inplace=True)
df['dcrmarketcap'].mask(df['dcrmarketcap'] == 0, df['CapMrktCurUSD'], inplace=True)

""" for i in df_early['date']: #swap in early price data
    #Add Early PriceUSD Data
     df.loc[df.date==i,'dcrusd'] = float(
        df_early.loc[df_early.date==i,'PriceUSD'])
     
     #Add Early PriceBTC Data
    df.loc[df.date==i,'dcrbtc'] = float(
        df_early.loc[df_early.date==i,'PriceBTC']
        )
    #Add Early MarketCap Data
    df.loc[df.date==i,'dcrmarketcap'] = (
        df.loc[df.date==i,'dcrusd'] * 
        df.loc[df.date==i,'supply']) """

# CALC METRICS

df['suppdiff'] = df['supply'].diff(1)
df['suppdiffusd'] = df['suppdiff'] * df['dcrusd']
df['cumsub'] = df['suppdiffusd'].cumsum()
df['powsub'] = df['cumsub'] * 0.6
df['possub'] = df['cumsub'] * 0.3
df['treassub'] = df['cumsub'] * 0.1
df['networkprofit'] = (df['dcrmarketcap'] - df['cumsub']) / df['cumsub']

df['dcrbtcmarketcap'] = df['dcrmarketcap'] / df['btcusd']
df['suppdiffbtc'] = df['suppdiffusd'] / df['btcusd']
df['cumsubbtc'] = df['suppdiffbtc'].cumsum()
df['powsubbtc'] = df['cumsubbtc'] * 0.6
df['possubbtc'] = df['cumsubbtc'] * 0.3
df['treassubbtc'] = df['cumsubbtc'] * 0.1
df['networkprofitbtc'] = (df['dcrbtcmarketcap'] - df['cumsubbtc']) / df['cumsubbtc']

print(df)

# plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('#E0E0E0')
fig.patch.set_alpha(0.7)
 
ax1.plot(df['date'], df['dcrmarketcap'], label='Decred Market Cap', color='black')
ax1.plot(df['date'], df['cumsub'], label='Cumulative Subsidy', linestyle=':', color='r')
ax1.plot(df['date'], df['powsub'], label='PoW Subsidy', linestyle=':', color='g')
ax1.plot(df['date'], df['possub'], label='PoS Subsidy', linestyle=':', color='b')
ax1.plot(df['date'], df['treassub'], label='Treasury Subsidy', linestyle=':', color='y')

ax1.set_yscale('log')
ax1.set_ylim(0, df['dcrmarketcap'].max()*3)
ax1.legend(loc='upper right')
ax1.grid()

ax2 = ax1.twinx()
ax2.plot(df['date'], df['networkprofit'], color='r', alpha=.5)

ax2.fill_between(df['date'], df['networkprofit'], where=df['networkprofit'] > 0, facecolor='blue', alpha=0.15)
ax2.fill_between(df['date'], df['networkprofit'], where=df['networkprofit'] < 0, facecolor='red', alpha=0.15)

ax2.set_ylabel('Network P/L on Subsidies Issued (%)')
ax2.set_ylim(-1, 30)

plt.title("DECRED NETWORK VALUE VS BLOCK SUBSIDIES ISSUED")
fig.tight_layout()
plt.show()