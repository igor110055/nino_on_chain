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
date_2 = "2020-07-20"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))
price.columns = ['date', 'PriceBTC']
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

print(df)

# PLOT

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'], df['28 Inflow'], label='28 Day Inflow / Outflow', color='aqua')
ax1.plot(df['date'], df['142 Inflow'], label='142 Day Inflow / Outflow', color='w')
ax1.fill_between(df['date'], df['28 Inflow'], where=df['28 Inflow'] > 0, facecolor='aqua', alpha=0.4)
ax1.fill_between(df['date'], df['28 Inflow'], where=df['28 Inflow'] < 0, facecolor='red', alpha=0.7)
ax1.set_facecolor('black')
ax1.set_title("Net Inflows & Outflow From Ticket Pool Over 28 & 142 Days", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel("DCR Net Inflow / Outflow", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
ax1.grid()
ax1.legend()

ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.plot(df['date'], df['PriceBTC'], color='w')
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