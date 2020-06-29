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
date_2 = "2020-06-28"

price = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)

# Clean CM data

cm_df = cmdc.cm_data_convert(price)
cm_df1 = cmdc.cm_date_format(price)

cm_df['date'] = cm_df1
cm_df['date'] = pd.to_datetime(cm_df['date'], utc=True)
cm_df['DCRBTC'] = cm_df[0]

# STAKE PARTICIPATION %

Stk_part = dcrdata.chart("stake-participation")
print(Stk_part.keys())

# Separate Stake participation and DCR Supply
Pool_part = Stk_part['poolval']
Dcr_circ = Stk_part['circulation']
Dcr_time = Stk_part['t']

# Convert to Pandas
df = pd.DataFrame(Pool_part) / 100000000
df_1 = pd.DataFrame(Dcr_circ) / 100000000

# Change From Unix to Datetime
df_2 = pd.to_datetime(Dcr_time, unit='s', utc=True)
df_2 = pd.DataFrame(df_2)

# Merge Datasets
df_2['Circulation'] = df_1
df_2['Participation'] = df
df_2['date'] = df_2[0]

stk_df = df_2.merge(cm_df, on='date', how='left')

# Calc Stake Pool % of Supply & INFLOW / OUTFLOW METRICS
percent_supply = df / df_1

inflow_14 = df_2['Participation'].diff(periods=14)
inflow_28 = df_2['Participation'].diff(periods=28)
inflow_142 = df_2['Participation'].diff(periods=142)

pct_28 = df_2['Participation'].pct_change(periods=28)
pct_142 = df_2['Participation'].pct_change(periods=142)

# Merge inflow data
stk_df['14 Inflow'] = inflow_14
stk_df['28 Inflow'] = inflow_28
stk_df['142 Inflow'] = inflow_142

stk_df['14infsupp'] = stk_df['14 Inflow'] / stk_df['Circulation']
stk_df['142infsupp'] = stk_df['142 Inflow'] / stk_df['Circulation']

stk_df['28 Change'] = pct_28
stk_df['142 Change'] = pct_142

# Print merged data and plot inflows / outflows
print(stk_df)

# Send merged data to excel
""" stk_df.to_excel('stakeflows1.xlsx') """

# PLOT

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)

ax1.plot(stk_df['date'], stk_df['28 Inflow'], label='28 Day Inflow / Outflow', color='aqua')
ax1.plot(stk_df['date'], stk_df['142 Inflow'], label='142 Day Inflow / Outflow', color='w')
ax1.fill_between(stk_df['date'], stk_df['28 Inflow'], where=stk_df['28 Inflow'] > 0, facecolor='aqua', alpha=0.4)
ax1.fill_between(stk_df['date'], stk_df['28 Inflow'], where=stk_df['28 Inflow'] < 0, facecolor='red', alpha=0.7)
ax1.set_facecolor('black')
ax1.set_title("Net Inflows & Outflow From Ticket Pool Over 28 & 142 Days", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel("DCR Net Inflow / Outflow", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
ax1.grid()
ax1.legend()

ax2 = plt.subplot(2, 1, 2, sharex=ax1)

ax2.plot(stk_df['date'], stk_df['DCRBTC'], color='w')
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