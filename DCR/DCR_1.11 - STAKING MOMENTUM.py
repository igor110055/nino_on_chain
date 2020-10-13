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
date_2 = "2020-10-13"

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

period = 142

df['adjpart'] = df['poolval'] / df['circulation']
df['adjpart142'] = df['adjpart'].rolling(period).mean()
df['ratio'] = df['adjpart'] / df['adjpart142']
df['poolval142'] = df['poolval'].rolling(period).mean()

df['stkgradient'] = ((df['adjpart'] - df['adjpart'].shift(periods=period, axis=0)) / period)

print(df)

# Plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)

ax1.plot(df['date'], df['adjpart'], color='w')
ax1.plot(df['date'], df['adjpart142'], color='aqua')

ax1.set_title("Staking Momentum (%)", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel("% of Supply in Ticket Pool", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_facecolor('black')
ax1.grid()
ax1.legend()

ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.plot(df['date'], df['dcrbtc'], color='w')
ax2.set_yscale('log')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_facecolor('black')
ax2.set_title("DCRBTC", fontsize=20, fontweight='bold', color='w')
ax2.axhspan(.0105, .0095, color='lime', alpha=0.75)
ax2.axhspan(.0016, .0014, color='m', alpha=0.75)
ax2.axhspan(.004, .0039, color='y', alpha=0.75)
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax2.set_ylabel("Price", fontsize=20, fontweight='bold', color='w')
ax2.grid()

plt.show()