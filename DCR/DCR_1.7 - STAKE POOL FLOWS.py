# COINMETRICS
import coinmetrics
import cm_data_converter as cmdc

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
date_2 = "2020-05-11"

price = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)

# Clean CM data

cm_df = cmdc.cm_data_convert(price)

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
df_2 = pd.to_datetime(Dcr_time, unit='s')
df_2 = pd.DataFrame(df_2)

# Merge Datasets
df_2['Circulation'] = df_1
df_2['Participation'] = df
df_2['DCRBTC'] = cm_df

# Calc Stake Pool % of Supply & INFLOW / OUTFLOW METRICS
percent_supply = df / df_1
inflow_28 = df_2['Participation'].diff(periods=28)
inflow_142 = df_2['Participation'].diff(periods=142)

pct_28 = df_2['Participation'].pct_change(periods=28)
pct_142 = df_2['Participation'].pct_change(periods=142)

# Merge inflow data
df_2['28 Inflow'] = inflow_28
df_2['142 Inflow'] = inflow_142

df_2['28 Change'] = pct_28
df_2['142 Change'] = pct_142

# Print merged data and plot inflows / outflows
print(df_2)

# Send merged data to excel
df_2.to_excel('stakeflows.xlsx')

plt.figure()
ax1 = plt.subplot(1,1,1)
plt.plot(df_2[0], inflow_28, label='28 Day Inflow / Outflow')
plt.plot(df_2[0], inflow_142, label='142 Day Inflow / Outflow')
plt.fill_between(df_2[0], inflow_28)
plt.title("Net Inflows & Outflow From Ticket Pool Over 28 & 142 Days")
plt.ylabel("DCR Net Inflow / Outflow")
plt.legend()


""" plt.subplot(2, 1, 2)
plt.plot(cm_df)
plt.yscale('log')
plt.title("DCRBTC") """
plt.show() 