import coinmetrics
import cm_data_converter as cmdc

# DCRDATA
from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")
import pandas as pd

# FORMAT EARLY PRICE DATA

filename = 'DCR/DCR_data.xlsx'
df_early = pd.read_excel(filename)
early = df_early[['date', 'PriceBTC']].copy()
early['date'] = pd.to_datetime(early['date'], utc=True)

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# Pull CM data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-06-05"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))
price.columns = ['date', 'dcrbtc']

# Merge early price data and CM data

price = price.merge(early, on='date', how='left')
price = price.fillna(0)

price['dcrbtc'].mask(price['dcrbtc'] == 0, early['PriceBTC'], inplace=True)

# Pull DCRDATA
atoms = 100000000
Stk_part = pd.DataFrame(dcrdata.chart("stake-participation"))
Stk_part = Stk_part.drop(columns=['axis', 'bin'])
Stk_part.columns = ['circulation', 'poolval', 'date']

Stk_part['date'] = pd.to_datetime(Stk_part['date'], unit='s', utc=True)
Stk_part['circulation'] = Stk_part['circulation'] / atoms
Stk_part['poolval'] = Stk_part['poolval'] / atoms

# Merge Data

df = price.merge(Stk_part, on='date', how='left')

# Calc Metrics

df['adjpart'] = df['poolval'] / df['circulation']
df['adjpart142'] = df['adjpart'].pct_change(142)

print(df)

# Plot

fig = plt.figure()
fig.patch.set_facecolor('#E0E0E0')
fig.patch.set_alpha(0.7)

ax1 = plt.subplot(2,1,1)
""" plt.plot(df['date'], df['adjpart']) """
plt.plot(df['date'], df['adjpart28'])
""" plt.plot(df['date'], df['adjpart28'])
plt.plot(df['date'], df['adjpart142']) """
""" plt.fill_between(stk_df['date'], stk_df['28 Inflow'], where=stk_df['28 Inflow'] > 0, facecolor='blue', alpha=0.25)
plt.fill_between(stk_df['date'], stk_df['28 Inflow'], where=stk_df['28 Inflow'] < 0, facecolor='red', alpha=0.25) """
plt.title("Staking Momentum (%)")
plt.ylabel("Percentage of Supply in Ticket Pool")
plt.grid()
plt.legend()

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(df['date'], df['dcrbtc'])
plt.yscale('log')
plt.title("DCRBTC")
plt.grid()
plt.show()