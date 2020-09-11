import coinmetrics
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib.ticker as ticker

from tinydecred.pydecred.dcrdata import DcrdataClient
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# PULL DATA
asset = "dcr"
asset1 = "btc"
date1 = "2016-06-01"
date2 = "2020-09-09"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

dcrmcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date1, date2))
btcmcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "CapMrktCurUSD", date1, date2))
dcrreal= cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapRealUSD", date1, date2))

df = dcrmcap.merge(btcmcap, on='date', how='left').merge(dcrreal, on='date', how='left')
df.columns = ['date', 'dcrmcap', 'btcmcap', 'dcrreal']

# Pull DCRDATA
atoms = 100000000
Stk_part = pd.DataFrame(dcrdata.chart("stake-participation"))
Stk_part = Stk_part.drop(columns=['axis', 'bin'])
Stk_part.columns = ['circulation', 'poolval', 'date']

Stk_part['date'] = pd.to_datetime(Stk_part['date'], unit='s', utc=True)
Stk_part['circulation'] = Stk_part['circulation'] / atoms
Stk_part['poolval'] = Stk_part['poolval'] / atoms

# Merge Data

df = df.merge(Stk_part, on='date', how='left')

# Calc Metrics

df['adjpart'] = df['poolval'] / df['circulation']
df['floatpart'] = (1 - df['adjpart'])

df['poolcap'] = df['dcrmcap'] * df['adjpart']
df['floatcap'] = df['dcrmcap'] * df['floatpart']

df['dcrbtcadj'] = df['dcrmcap'] / df['btcmcap']
df['pooldcrbtc'] = df['poolcap'] / df['btcmcap']
df['floatdcrbtc'] = df['floatcap'] / df['btcmcap']

print(df)

# Plot

name = "@permabullnino"
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'], df['dcrmcap'], color='w', label='Decred Market Cap')
ax1.plot(df['date'], df['poolcap'], color='aqua', label='Pool Cap')
ax1.plot(df['date'], df['floatcap'], color='red', label='Float Cap')
ax1.plot(df['date'], df['dcrreal'], color='lime', label='Decred Realized Cap')
ax1.set_ylabel("Network Value", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Market Cap Comparison", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend(edgecolor='w')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(df['date'], df['dcrbtcadj'], color='w', label='Adj DCRBTC')
ax2.plot(df['date'], df['pooldcrbtc'], color='aqua', label='Pool DCRBTC')
ax2.plot(df['date'], df['floatdcrbtc'], color='red', label='Float DCRBTC')
ax2.set_ylabel("DCRBTC Values", fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.legend(loc='upper right')
ax2.set_facecolor('black')
ax2.set_yscale('log')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax2.set_title("Market Cap Values Divided by Bitcoin Market Cap", fontsize=20, fontweight='bold', color='w')
ax2.grid()

plt.show()