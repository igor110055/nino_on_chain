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
date_2 = "2020-07-10"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
pricebtc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))
price = price.merge(pricebtc, on='date', how='left')
price['date'] = pd.to_datetime(price['date'], unit='s', utc=True).dt.strftime('%Y-%m-%d')

# Merge dcrdata and cmdata

df = df.merge(price, on='date', how='left')
df = df.drop(columns=['window'])
df.columns = ['tixvol', 'tixprice', 'date', 'dcrvol', 'PriceUSD', 'PriceBTC']
df['date'] = pd.to_datetime(df['date'])

# Calc metrics

df['tixpriceusd'] = df['tixprice'] * df['PriceUSD']
df['tixpricebtc'] = df['tixprice'] * df['PriceBTC']

df['tixpriceusd142'] = df['tixpriceusd'].rolling(142).mean()
df['tixpricebtc142'] = df['tixpricebtc'].rolling(142).mean()

df['dcrvolusd'] = df['dcrvol'] * df['PriceUSD']
df['dcrvolbtc'] = df['dcrvol'] * df['PriceBTC']

print(df)

# Plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'], df['tixpricebtc'], label='Ticket Cost BTC', color='w')
ax1.plot(df['date'], df['tixpricebtc142'], label='Ticket Cost BTC 142 Avg', color='lime')
ax1.set_ylabel("BTC Value", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.set_title("Ticket Cost BTC", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.tick_params(color='w', labelcolor='w')
ax1.grid()
ax1.legend()
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax11 = ax1.twinx()
ax11.bar(df['date'], df['dcrvolbtc'], color='aqua')
ax11.set_ylabel("BTC Tix Vol", fontsize=20, fontweight='bold', color='w')
ax11.tick_params(color='w', labelcolor='w')
ax11.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.plot(df['date'], df['tixpriceusd'], label='Ticket Cost USD', color='w')
ax2.plot(df['date'], df['tixpriceusd142'], label='Ticket Cost USD 142 Avg', color='lime')
ax2.set_facecolor('black')
ax2.set_title("Ticket Cost USD", fontsize=20, fontweight='bold', color='w')
ax2.set_ylabel("USD Value", fontsize=20, fontweight='bold', color='w')
ax2.legend()
ax2.tick_params(color='w', labelcolor='w')
ax2.set_yscale('log')
ax2.grid()
for axis in [ax2.yaxis]:
    axis.set_major_formatter(ScalarFormatter())

ax22 = ax2.twinx()
ax22.bar(df['date'], df['dcrvolusd'], color='aqua')
ax22.set_ylabel("USD Tix Vol", fontsize=20, fontweight='bold', color='w')
ax22.tick_params(color='w', labelcolor='w')
ax22.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

plt.show()