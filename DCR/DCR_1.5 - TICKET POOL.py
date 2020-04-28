# DCRDATA
from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")
import pandas as pd

# COINMETRICS
import coinmetrics
import cm_data_converter

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#Fetch data
date_1 = "2016-05-17"
date_2 = "2020-04-24"
price = cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2)
#clean data
price_clean = cm_data_converter.cm_data_convert(price)
#convert to pandas
df_precio = pd.DataFrame(price_clean)

#### DIVIDE BETWEEN CM AND DCRDATA ####

# STAKE PARTICIPATION %

Stk_part = dcrdata.chart("stake-participation")
#print(Stk_part.keys())

# Separate Stake participation and DCR Supply
Pool_part = Stk_part['poolval']
Dcr_circ = Stk_part['circulation']

# Convert to Pandas
df = pd.DataFrame(Pool_part)
df_1 = pd.DataFrame(Dcr_circ)

# Calc Stake Pool % of Supply
df_2 = df / df_1

# Calc Stake Pool % of Supply MA & Ratio
MA_ = df_2.rolling(window=284).mean()
ratio = df_2 / MA_

# Merge DCRBTC & DCRUSD Data to compare, & Print to check values
ratio['DCRUSD'] = df_precio
ratio['Raw Value of % Staked'] = df_2
print(ratio)
"""ISSUES MERGING THE DATASETS (LINING UP THE START AND END OF DATASET), CLEAN UP"""
# Pull to Excel worksheet
ratio.to_excel('ticket_pool.xlsx')

# Plot values to check indicator
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(ratio[0])
plt.title("Ticket Pool Ratio")

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(ratio['DCRUSD'])
plt.title("DCRUSD")
plt.yscale('log')
plt.show()