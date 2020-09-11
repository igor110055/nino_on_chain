import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib as mpl

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

#fetch desired data
date_1 = "2016-02-01"
date_2 = "2020-09-10"

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

# CALC METRICS

#subpaidusd
df['suppdiff'] = df['supply'].diff(1)
df['suppdiffusd'] = df['suppdiff'] * df['dcrusd']

df['suppissue'] = df['suppdiff'].cumsum()

df['cumsub'] = df['suppdiffusd'].cumsum()
df['powsub'] = df['cumsub'] * 0.6
df['possub'] = df['cumsub'] * 0.3
df['treassub'] = df['cumsub'] * 0.1
df['networkprofit'] = (df['dcrmarketcap'] - df['cumsub']) / df['cumsub']

#subpaidbtc
df['dcrbtcmarketcap'] = df['dcrmarketcap'] / df['btcusd']
df['suppdiffbtc'] = df['suppdiffusd'] / df['btcusd']

df['cumsubbtc'] = df['suppdiffbtc'].cumsum()
df['powsubbtc'] = df['cumsubbtc'] * 0.6
df['possubbtc'] = df['cumsubbtc'] * 0.3
df['treassubbtc'] = df['cumsubbtc'] * 0.1
df['networkprofitbtc'] = (df['dcrbtcmarketcap'] - df['cumsubbtc']) / df['cumsubbtc']

#totalsubusd
issue = 21000000 - 1680000
df['percissue'] = df['suppissue'] / issue
df['issfactor'] = 1 / df['percissue']

df['totsub'] = df['cumsub'] * df['issfactor']
df['totpow'] = df['powsub'] * df['issfactor']
df['totpos'] = df['possub'] * df['issfactor']
df['tottreas'] = df['treassub'] * df['issfactor']
df['totnetworkprofit'] = (df['dcrmarketcap'] - df['totsub']) / df['totsub']

#totalsubbtc
df['totsubbtc'] = df['cumsubbtc'] * df['issfactor']
df['totpowbtc'] = df['powsubbtc'] * df['issfactor']
df['totposbtc'] = df['possubbtc'] * df['issfactor']
df['tottreasbtc'] = df['treassubbtc'] * df['issfactor']
df['totnetworkprofitbtc'] = (df['dcrbtcmarketcap'] - df['totsubbtc']) / df['totsubbtc']

#remsubusd
df['remtotusd'] = df['totsub'] - df['cumsub']
df['rempowusd'] = df['totpow'] - df['powsub']
df['remposusd'] = df['totpos'] - df['possub']
df['remtreasusd'] = df['tottreas'] - df['treassub']

print(df)

# plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

# subsidy paid chart

""" ax1.plot(df['date'], df['dcrmarketcap'], label='Decred Market Cap', color='w')
ax1.plot(df['date'], df['cumsub'], label='Cumulative Subsidy', linestyle=':', color='aqua')
ax1.plot(df['date'], df['powsub'], label='PoW Subsidy', linestyle=':', color='r')
ax1.plot(df['date'], df['possub'], label='PoS Subsidy', linestyle=':', color='m')
ax1.plot(df['date'], df['treassub'], label='Treasury Subsidy', linestyle=':', color='y')

ax1.set_yscale('log')
ax1.set_facecolor('black')
ax1.set_ylim(0, df['dcrmarketcap'].max()*3)
ax1.legend(loc='right')
ax1.grid()
ax1.set_title("Market Cap vs Block Subsidies", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel('Network Value', fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

""" ax2 = ax1.twinx()
ax2.plot(df['date'], df['networkprofit'], color='aqua', alpha=1)

ax2.fill_between(df['date'], df['networkprofit'], where=df['networkprofit'] > 0, facecolor='aqua', alpha=0.4)
ax2.fill_between(df['date'], df['networkprofit'], where=df['networkprofit'] < 0, facecolor='red', alpha=0.4)

ax2.set_ylabel('Network P/L on Subsidies Issued (%)', fontsize=20, fontweight='bold', color='w')
ax2.set_ylim(-1, 30)
ax2.tick_params(color='w', labelcolor='w') """

# total subisdy chart usd

""" ax1.plot(df['date'], df['dcrmarketcap'], label='Decred Market Cap', color='w')
ax1.plot(df['date'], df['totsub'], label='Cumulative Subsidy', color='aqua')
ax1.plot(df['date'], df['totpow'], label='PoW Subsidy', color='r')
ax1.plot(df['date'], df['totpos'], label='PoS Subsidy', color='m')
ax1.plot(df['date'], df['tottreas'], label='Treasury Subsidy', color='y')

ax1.set_yscale('log')
ax1.set_facecolor('black')
ax1.set_ylim(0, df['dcrmarketcap'].max()*3)
ax1.legend(loc='upper left')
ax1.grid()
ax1.set_title("Market Cap vs Block Subsidies", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel('Network Value', fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

""" ax2 = ax1.twinx()
ax2.plot(df['date'], df['totnetworkprofit'], color='aqua', alpha=1)

ax2.fill_between(df['date'], df['totnetworkprofit'], where=df['totnetworkprofit'] > 0, facecolor='aqua', alpha=0.4)
ax2.fill_between(df['date'], df['totnetworkprofit'], where=df['totnetworkprofit'] < 0, facecolor='red', alpha=0.4)

ax2.set_ylabel('Network P/L on Subsidies Issued (%)', fontsize=20, fontweight='bold', color='w')
ax2.set_ylim(-1, 30)
ax2.tick_params(color='w', labelcolor='w') """

# total subisdy chart btc

""" ax1.plot(df['date'], df['dcrbtcmarketcap'], label='Decred Market Cap', color='w')
ax1.plot(df['date'], df['totsubbtc'], label='Cumulative Subsidy', color='aqua')
ax1.plot(df['date'], df['totpowbtc'], label='PoW Subsidy', color='r')
ax1.plot(df['date'], df['totposbtc'], label='PoS Subsidy', color='m')
ax1.plot(df['date'], df['tottreasbtc'], label='Treasury Subsidy', color='y')

ax1.set_yscale('log')
ax1.set_facecolor('black')
ax1.set_ylim(0, df['dcrbtcmarketcap'].max()*2)
ax1.legend(loc='upper left')
ax1.grid()
ax1.set_title("Market Cap vs Block Subsidies", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel('Network Value', fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = ax1.twinx()
ax2.plot(df['date'], df['totnetworkprofitbtc'], color='aqua', alpha=1)

ax2.fill_between(df['date'], df['totnetworkprofitbtc'], where=df['totnetworkprofitbtc'] > 0, facecolor='aqua', alpha=0.4)
ax2.fill_between(df['date'], df['totnetworkprofitbtc'], where=df['totnetworkprofitbtc'] < 0, facecolor='red', alpha=0.4)

ax2.set_ylabel('Network P/L on Subsidies Issued (%)', fontsize=20, fontweight='bold', color='w')
ax2.set_ylim(-1, 30)
ax2.tick_params(color='w', labelcolor='w') """

# remaining subsidy usd

ax1.plot(df['date'], df['dcrmarketcap'], label='Decred Market Cap', color='w')
ax1.plot(df['date'], df['remtotusd'], label='Cumulative Subsidy', color='aqua')
ax1.plot(df['date'], df['rempowusd'], label='PoW Subsidy', color='r')
ax1.plot(df['date'], df['remposusd'], label='PoS Subsidy', color='m')
ax1.plot(df['date'], df['remtreasusd'], label='Treasury Subsidy', color='y')

ax1.set_yscale('log')
ax1.set_facecolor('black')
ax1.set_ylim(0, df['dcrmarketcap'].max()*3)
ax1.legend(loc='upper left')
ax1.grid()
ax1.set_title("Market Cap vs Block Subsidies", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel('Network Value', fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

plt.show()