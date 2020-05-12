# DCRDATA
from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")
import pandas as pd

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

# Calc Stake Pool % of Supply & INFLOW / OUTFLOW METRICS
percent_supply = df / df_1
inflow_28 = df_2['Participation'].diff(periods=63)
inflow_142 = df_2['Participation'].diff(periods=142)

# Merge inflow data
df_2['28 Inflow'] = inflow_28
df_2['142 Inflow'] = inflow_142

# Print merged data and plot inflows / outflows
print(df_2)

plt.plot(df_2[0], inflow_28, label='28 Day Inflow / Outflow')
plt.plot(df_2[0], inflow_142, label='142 Day Inflow / Outflow')
plt.title("Net Inflows & Outflow From Ticket Pool Over 28 & 142 Days")
plt.legend()
plt.show()