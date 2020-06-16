import coinmetrics
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc

from tinydecred.pydecred.dcrdata import DcrdataClient
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# PULL DATA
asset = "dcr"
asset1 = "btc"
date1 = "2010-01-01"
date2 = "2020-06-14"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

dcrusd = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date1, date2))
dcrmcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date1, date2))
dcrreal= cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapRealUSD", date1, date2))
dcrsupply = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "SplyCur", date1, date2))
btcsupply = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset1, "SplyCur", date1, date2))

df = dcrreal.merge(dcrusd, on='date', how='left').merge(dcrmcap, on='date', how='left').merge(dcrsupply, on='date', how='left').merge(btcsupply, on='date', how='left')
df.columns = ['date', 'dcrreal', 'dcrusd', 'dcrmcap', 'dcrsupply', 'btcsupply']

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
df['dcradjsupply'] = df['btcsupply'] / df['dcrsupply']
df['downcap'] = (1 - df['adjpart']) * df['dcrreal']
df['upcap'] = (1 / df['adjpart']) * df['dcrreal']

print(df)

# plot

name = "@permabullnino"
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
line1 = ax1.plot(df['date'], df['dcrmcap'], color='w')
line2 = ax1.plot(df['date'], df['dcrreal'], color='aqua')
line3 = ax1.plot(df['date'], df['upcap'], color='lime')
line4 = ax1.plot(df['date'], df['downcap'], color='lime')
ax1.set_ylabel("Network Value", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("HODL POWER", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend(edgecolor='w')

ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(df['date'], df['adjpart'], color='w')
ax2.set_ylabel("Stake Participation", fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_title("% of DCR Supply in Tickets", fontsize=20, fontweight='bold', color='w')
ax2.set_facecolor('black')
ax2.grid()
ax2.legend()

plt.show()