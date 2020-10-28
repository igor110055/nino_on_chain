# COINMETRICS
import coinmetrics
import cm_data_converter as cmdc
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

# DCRDATA
from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")
import pandas as pd

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# Pull data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-10-26"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))

price.columns = ['date', 'DCRBTC']

# FEE DATA
df = pd.DataFrame(dcrdata.chart("fees"))
df = df.drop(columns=['axis', 'bin'])
df['t'] = pd.to_datetime(df['t'], unit='s', utc='True')
df.columns = ['fees', 'date']
df['fees'] = df['fees'] / 100000000

# MERGE

df = df.merge(price, on='date', how='left')

# CALC METRICS
avg1 = 14
avg2 = 142

df['fees28'] = df['fees'].rolling(avg1).mean()
df['fees142'] = df['fees'].rolling(avg2).mean()

print(df)

# PLOT

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'], df['fees28'], label= str(avg1) + ' Day Fee Avg', color='aqua')
ax1.plot(df['date'], df['fees142'], label=str(avg2) + ' Day Fee Avg', color='lime')
ax1.set_yscale('log')
ax1.set_facecolor('black')
ax1.set_title("Fee Averages " + str(avg1) + " & " + str(avg2), fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel("Avg Daily Fees", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend()
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.plot(df['date'], df['DCRBTC'], color='w')
ax2.set_facecolor('black')
ax2.set_yscale('log')
ax2.set_title("DCRBTC Price", fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
ax2.axhspan(.0105, .0095, color='lime', alpha=0.75)
ax2.axhspan(.0016, .0014, color='m', alpha=0.75)
ax2.axhspan(.004, .0039, color='y', alpha=0.75)
ax2.set_ylabel("DCRBTC Price", fontsize=20, fontweight='bold', color='w')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax2.grid()

plt.show() 