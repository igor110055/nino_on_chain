# DCRDATA
from tinydecred.pydecred.dcrdata import DcrdataClient
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List the assets Coin Metrics has data for.
supported_assets = cm.get_supported_assets()
print("supported assets:\n", supported_assets)

# List all available metrics for DCR.
asset = "dcr"
date1 = "2016-02-08"
date2 = "2020-05-24"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

# retrieve the historical data for realized cap / market cap & merge cata

real_cap = cm.get_real_cap(asset, date1, date2)
mcap = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date1, date2)

df = cmdc.combo_convert(real_cap)
df1 = cmdc.combo_convert(mcap)

df = df.merge(df1, on='date', how='left')

# DCRDATA FORMATTING + CM DATA MERGE

Stk_part = dcrdata.chart("stake-participation")
df2 = pd.DataFrame(Stk_part)

df2 = df2.drop(columns=['axis', 'bin'])
df2.columns = ['circulation', 'poolval', 'date']

df2['circulation'] = df2['circulation'] / 100000000
df2['poolval'] = df2['poolval'] / 100000000

df2['date'] = pd.to_datetime(df2['date'], unit='s', utc=True)

df = df.merge(df2, on='date', how='left')

df.columns = ['date', 'realizedcap', 'marketcap', 'circulation', 'poolval']

print(df)

# CALC METRICS

df['28 Inflow'] = df['poolval'].diff(periods=28)    # net inflow / outflow of dcr in the ticket pool

df['unrealizedcap'] = df['marketcap'] - df['realizedcap']

df['unrealmarketcap'] = df['unrealizedcap'] / df['marketcap']

df['unrealizedchange'] = df['unrealizedcap'].pct_change(periods=28) # % change in unrealized profit / loss

df['aggPL'] = df['unrealizedcap'].rolling(28).sum()  # select a timeframe to see aggregate profit of stakeholders

df['expectedvalue'] = (df['unrealizedcap'] / df['poolval']) #unrealized p/l per dcr in ticket pool

df['realizedtop'] = df['realizedcap'] * 2

df['realizedbottom'] = df['realizedcap'] * 0.5

print(df) 

# PLOT

plt.figure()
ax1 = plt.subplot(2,1,1)
plt.plot(df['date'], df['unrealmarketcap'])
plt.fill_between(df['date'], df['unrealmarketcap'], where=df['unrealmarketcap'] > 0, facecolor='blue', alpha=0.25)
plt.fill_between(df['date'], df['unrealmarketcap'], where=df['unrealmarketcap'] < 0, facecolor='red', alpha=0.25)
plt.title("Unrealized P/L")
plt.grid()
plt.legend()

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df['date'], df['marketcap'], label='Market Cap')
plt.plot(df['date'], df['realizedcap'], label='Realized Cap')
plt.plot(df['date'], df['realizedtop'], label='Realized Top')
plt.plot(df['date'], df['realizedbottom'], label='Realized Bottom')
plt.fill_between(df['date'], df['realizedcap'], df['realizedtop'], where=df['realizedcap'] < df['realizedtop'], facecolor='green', alpha=0.15)
plt.fill_between(df['date'], df['realizedcap'], df['realizedbottom'], where=df['realizedcap'] > df['realizedbottom'], facecolor='red', alpha=0.15)
plt.yscale('log')
plt.title("Market Cap vs Realized Cap")
plt.grid()
plt.legend()
plt.show() 