# COINMETRICS
import coinmetrics
import cm_data_converter as cmdc
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

# GENERAL

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

#   TICKET DATA
ticketPrice = dcrdata.chart("ticket-price")
df = pd.DataFrame(ticketPrice)

# convert atoms to dcr, calc dcr in tix vol, and convert to datetime
df['price'] = df['price'] / 100000000
df['dcrtixvol'] = df['price'] * df['count'] 
df['t'] = pd.to_datetime(df['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d')
df.rename(columns={'t': 'date'}, inplace=True)

# COINMETRICS

cm = coinmetrics.Community()

# Pull data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-07-17"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
pricebtc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))
supply = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "SplyCur", date_1, date_2))
price = price.merge(pricebtc, on='date', how='left').merge(supply, on='date', how='left')
price['date'] = pd.to_datetime(price['date'], unit='s', utc=True).dt.strftime('%Y-%m-%d')

# Merge dcrdata and cmdata

df = df.merge(price, on='date', how='left')
df = df.drop(columns=['window'])
df.columns = ['tixvol', 'tixprice', 'date', 'dcrvol', 'PriceUSD', 'PriceBTC', 'Supply']
df['date'] = pd.to_datetime(df['date'])

# Calc Metrics

df['142hodl'] = df['dcrvol'].rolling(142).sum()
df['28hodl'] = df['dcrvol'].rolling(28).sum()

df['142hodladj'] = df['142hodl'] * df['PriceBTC']
df['28hodladj'] = df['28hodl'] * df['PriceBTC']

df['142hodladjusd'] = df['142hodl'] * df['PriceUSD']
df['28hodladjusd'] = df['28hodl'] * df['PriceUSD']

df['28volratio'] = df['28hodladjusd'].max() / df['28hodladjusd']
df['PriceUSDratio'] = df['PriceUSD'].max() / df['PriceUSD']

df['dcrtixsum'] = df['dcrvol'].cumsum()
df['wtdcrvol'] = df['dcrvol'] / df['dcrtixsum'].iloc[-1]
df['wtdcrvolsum'] = df['wtdcrvol'].cumsum()

print(df)

# Plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'], df['PriceUSD'], color='w')
ax1.set_ylabel("DCRUSD Price", fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_facecolor('black')
ax1.set_yscale('log')
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax11 = ax1.twinx()
ax11.bar(df['date'], df['28hodladjusd'], label='28 USD Vol', color='aqua')
""" ax11.plot(df['date'], df['142hodladj'], label='142 HODL', color='lime') """
ax11.set_ylabel("Volume", fontsize=20, fontweight='bold', color='w')
ax11.set_title("DCRUSD vs Ticket Volume Denominated in USD", fontsize=20, fontweight='bold', color='w')
""" ax11.set_yscale('log') """
ax11.tick_params(color='w', labelcolor='w')
ax11.legend()
ax11.grid()
ax11.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot(df['date'], df['PriceBTC'], color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_ylabel('DCBTC Price', fontsize=20, fontweight='bold', color='w')
ax2.set_title('DCRBTC vs Ticket Volume Denominated in BTC', fontsize=20, fontweight='bold', color='w')
ax2.set_facecolor('black')
ax2.legend()
ax2.set_yscale('log')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax22 = ax2.twinx()
ax22.bar(df['date'], df['wtdcrvolsum'], label='28 BTC Vol', color='aqua', alpha=0.5)
""" ax11.plot(df['date'], df['142hodladj'], label='142 HODL', color='lime') """
ax22.set_ylabel("Volume", fontsize=20, fontweight='bold', color='w')
ax22.set_title("DCRBTC vs Ticket Volume Denominated in BTC", fontsize=20, fontweight='bold', color='w')
""" ax11.set_yscale('log') """
ax22.tick_params(color='w', labelcolor='w')
ax22.legend()
ax22.grid()
""" ax22.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

plt.show()