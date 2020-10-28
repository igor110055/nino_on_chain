# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd
import cm_data_converter as cmdc
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter
import matplotlib as mpl

df = pd.DataFrame()

df['weeks'] = range(105)

# set price lists

pricelist = [10,20,40,80,160,320,640,1280]

for price in pricelist:
    df[price] = df['weeks'] * price

btcpricelist = [.001,.002,.004,.008,.016,.02,.024,.028]

for btcprice in btcpricelist:
    df[btcprice] = df['weeks'] * btcprice

print(df)

# PLOT VALUES

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['weeks'], df[10], label= '$10 Sells: ' + str(round(df[10].iloc[-1],0)), color='w')
ax1.plot(df['weeks'], df[20], label= '$20 Sells :' + str(round(df[20].iloc[-1],0)), color='orange')
ax1.plot(df['weeks'], df[40], label= '$40 Sells :' + str(round(df[40].iloc[-1],0)), color='y')
ax1.plot(df['weeks'], df[80], label= '$80 Sells :' + str(round(df[80].iloc[-1],0)), color='r')
ax1.plot(df['weeks'], df[160], label= '$160 Sells :' + str(round(df[160].iloc[-1],0)), color='m')
ax1.plot(df['weeks'], df[320], label= '$320 Sells :' + str(round(df[320].iloc[-1],0)), color='blue')
ax1.plot(df['weeks'], df[640], label= '$640 Sells :' + str(round(df[640].iloc[-1],0)), color='aqua')
ax1.plot(df['weeks'], df[1280], label= '$1280 Sells :' + str(round(df[1280].iloc[-1],0)), color='lime')
ax1.set_ylabel("USD Savings", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Staking Income Planning for DCR", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend()
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(df['weeks'], df[.001], label= '.001 Sells: ' + str(round(df[.001].iloc[-1],3)), color='w')
ax2.plot(df['weeks'], df[.002], label= '.002 Sells :' + str(round(df[.002].iloc[-1],3)), color='orange')
ax2.plot(df['weeks'], df[.004], label= '.004 Sells :' + str(round(df[.004].iloc[-1],3)), color='y')
ax2.plot(df['weeks'], df[.008], label= '.008 Sells :' + str(round(df[.008].iloc[-1],3)), color='r')
ax2.plot(df['weeks'], df[.016], label= '.016 Sells :' + str(round(df[.016].iloc[-1],3)), color='m')
ax2.plot(df['weeks'], df[.02], label= '.02 Sells :' + str(round(df[.02].iloc[-1],3)), color='blue')
ax2.plot(df['weeks'], df[.024], label= '.024 Sells :' + str(round(df[.024].iloc[-1],3)), color='aqua')
ax2.plot(df['weeks'], df[.028], label= '.028 Sells :' + str(round(df[.028].iloc[-1],3)), color='lime')
ax2.set_ylabel("BTC Savings", fontsize=20, fontweight='bold', color='w')
ax2.set_facecolor('black')
ax2.set_title("Staking Income Planning for DCR", fontsize=20, fontweight='bold', color='w')
ax2.set_yscale('log')
ax2.tick_params(color='w', labelcolor='w')
ax2.grid()
ax2.legend()
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

plt.show()