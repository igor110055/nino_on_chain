import coinmetrics
import cm_data_converter as cmdc
import matplotlib as mpl
import matplotlib.ticker as ticker

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
date_2 = "2020-07-20"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))
price.columns = ['date', 'dcrbtc']

# Merge early price data and CM data

""" price = price.merge(early, on='date', how='left')
price = price.fillna(0)

price['dcrbtc'].mask(price['dcrbtc'] == 0, early['PriceBTC'], inplace=True) """

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
earlsupp = 1680000
final = 21000000 - earlsupp
pos = 0.3
final_pos = final * pos

df['curr_pos'] = (df['circulation'] - earlsupp) * pos
df['rem_pos'] = final_pos - df['curr_pos']
df['scarce_ratio'] = df['poolval'] / df['rem_pos']

print(df)

# Plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(1,1,1)
ax1.bar(df['date'], df['scarce_ratio'], color='lime', alpha=0.5)
ax1.set_title("Scarcity vs DCRBTC Price", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel("Scarcity (DCR)", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_facecolor('black')
ax1.grid()
""" ax1.legend() """
""" ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

ax11 = ax1.twinx()
ax11.plot(df['date'], df['dcrbtc'], color='w')
ax11.set_yscale('log')
ax11.tick_params(color='w', labelcolor='w')
ax11.set_facecolor('black')
ax11.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax11.set_ylabel("Price", fontsize=20, fontweight='bold', color='w')

plt.show()