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

df['trade'] = range(10)

# set return lists

returnlist = [.10,.20,.30,.40,.50,1]

for gain in returnlist:
    df[gain] = (1 + gain)**df['trade']

print(df)

# PLOT VALUES

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
ax1.plot(df['trade'], df[0.10], label= '10% Return Compounded: ' + str(round(df[0.10].iloc[-1],0)), color='w')
ax1.plot(df['trade'], df[0.20], label= '20% Return Compounded: ' + str(round(df[0.20].iloc[-1],0)), color='r')
ax1.plot(df['trade'], df[0.30], label= '30% Return Compounded: ' + str(round(df[0.30].iloc[-1],0)), color='y')
ax1.plot(df['trade'], df[0.40], label= '40% Return Compounded: ' + str(round(df[0.40].iloc[-1],0)), color='m')
ax1.plot(df['trade'], df[0.50], label= '50% Return Compounded: ' + str(round(df[0.50].iloc[-1],0)), color='aqua')
ax1.plot(df['trade'], df[1], label= '100% Return Compounded: ' + str(round(df[1].iloc[-1],0)), color='lime')
ax1.set_ylabel("Return", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Return on $1 Compounded Over 10 Trades @ Different Return %s", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend()
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

plt.show()