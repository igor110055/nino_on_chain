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
date_2 = "2021-12-26"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))
mcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))

price = price.merge(mcap, on='date', how='left')
price.columns = ['date', 'PriceBTC', 'mcap']
# STAKE PARTICIPATION DATA

df = pd.DataFrame(dcrdata.chart("stake-participation"))
df = df.drop(columns=['axis', 'bin', 'circulation'])
df['t'] = pd.to_datetime(df['t'], unit='s', utc='True')
df['poolval'] = df['poolval'] / 100000000
df.columns = ['poolval', 'date']

df = df.merge(price, on='date', how='left')

# Calc Metrics

df['28 Inflow'] = df['poolval'].diff(28)
df['142 Inflow'] = df['poolval'].diff(142)

df['28btc'] = df['28 Inflow'] * df['PriceBTC']

df['28mcap'] = df['mcap'].diff(28)
df['142mcap'] = df['mcap'].diff(142)

df['28imp'] = df['mcap'] / df['28 Inflow']
df['142imp'] = df['mcap'] / df['142 Inflow']


print(df)

# PLOT

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
ax1.plot(df['date'], df['28 Inflow'], label='28 Day Inflow / Outflow: ' + str(round(df['28 Inflow'].iloc[-1],0)), color='aqua')
ax1.plot(df['date'], df['142 Inflow'], label='142 Day Inflow / Outflow: ' + str(round(df['142 Inflow'].iloc[-1],0)), color='w')
ax1.fill_between(df['date'], df['28 Inflow'], where=df['28 Inflow'] > 0, facecolor='aqua', alpha=0.4)
ax1.fill_between(df['date'], df['28 Inflow'], where=df['28 Inflow'] < 0, facecolor='red', alpha=0.7)
ax1.set_facecolor('black')
ax1.set_title("Net Inflows & Outflow From Ticket Pool Over 28 Days vs DCRBTC Price", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel("DCR Net Inflow / Outflow", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
ax1.grid()
ax1.legend()
ax1.set_ylim(df['28 Inflow'].min(),df['142 Inflow'].max()*2)

ax2 = ax1.twinx()
ax2.plot(df['date'], df['PriceBTC'], color='w', label='Price: ' + str(round(df['PriceBTC'].iloc[-1],6)))
ax2.set_facecolor('black')
ax2.set_yscale('log')
""" ax2.set_title("DCRBTC Price", fontsize=20, fontweight='bold', color='w') """
ax2.tick_params(color='w', labelcolor='w')
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
""" ax2.axhspan(.0105, .0095, color='lime', alpha=0.75)
ax2.axhspan(.0012, .001, color='m', alpha=0.75)
ax2.axhspan(.004, .0039, color='y', alpha=0.75) """
ax2.set_ylabel("DCRBTC Price", fontsize=20, fontweight='bold', color='w')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
""" ax2.grid() """
ax2.legend(loc='upper left')
ax2.set_ylim(df['PriceBTC'].min()/2,df['PriceBTC'].max())

plt.show() 