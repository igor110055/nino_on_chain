from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime as dt
import cm_data_converter as cmdc
import coinmetrics 
import matplotlib.ticker as ticker
import matplotlib as mpl

dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

#   TICKET DATA
ticketPrice = dcrdata.chart("ticket-price")
print(ticketPrice.keys())

# Convert to pandas
tix = pd.DataFrame(ticketPrice)

tix['t'] = pd.to_datetime(tix['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d')

tix = tix.drop(columns=['window'])

tix.columns = ['tixvol', 'tixprice', 'date']

# COINMETRICS DATA

cm = coinmetrics.Community()

# Add early price data

filename = 'DCR/DCR_data.xlsx'
df_early = pd.read_excel(filename)
early = df_early[['date', 'PriceUSD', 'PriceBTC', 'CapMrktCurUSD']].copy()
early['date'] = pd.to_datetime(early['date'], utc=True)
early.columns = ['date', 'dcrusd', 'dcrbtc', 'mcap']

# Pull data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2021-12-27"
metric = "PriceUSD"
metric1 = "PriceBTC"
metric2 = "CapMrktCurUSD"
metric3 = "CapRealUSD"
metric4 = "BlkSizeByte"
metric5 = "SplyCur"

metriclist = [metric, metric1, metric2, metric3, metric4, metric5]

df = pd.DataFrame(columns=['date'])

for item in metriclist:
    df1 = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, item, date_1, date_2))
    df1.columns = ['date', item]
    df = df.merge(df1, on='date', how='outer')

df['date'] = df['date'].dt.strftime('%Y-%m-%d') #convert to string format for merging purposes

# MERGE DATASETS
df = tix.merge(df, on='date', how='left')

df['date'] = pd.to_datetime(df['date'], utc=True)

df = df.merge(early, on='date', how='left')
df = df.fillna(0)

df['PriceUSD'].mask(df['PriceUSD'] == 0, df['dcrusd'], inplace=True)
df['PriceBTC'].mask(df['PriceBTC'] == 0, df['dcrbtc'], inplace=True)
df['CapMrktCurUSD'].mask(df['CapMrktCurUSD'] == 0, df['mcap'], inplace=True)

# Calc Metrics

#convert ticket price from atoms to dcr
atoms = 100000000
df['tixprice'] = df['tixprice'] / atoms

#realcap --> realprice
df['realdcrusd'] = df['CapRealUSD'] / df['SplyCur']

#dcrvol metrics
sum1 = 56
sum2 = 112
sum3 = 284

df['btcPriceUSD'] = df['PriceUSD'] / df['PriceBTC']

df['dcrvol'] = df['tixprice'] * df['tixvol']
df['dcrvolcum'] = df['dcrvol'].cumsum()
df['dcrvolsum1'] = df['dcrvol'].rolling(sum1).sum()
df['dcrvolsum2'] = df['dcrvol'].rolling(sum2).sum()
df['dcrvolsum3'] = df['dcrvol'].rolling(sum3).sum()
df['volratio1'] = df['dcrvolsum1'] / df['dcrvolsum2']
df['volratio2'] = df['dcrvolsum1'] / df['dcrvolsum3']

#btc metrics
df['realdcrbtc'] = df['realdcrusd'] / df['btcPriceUSD'].rolling(21).mean()
df['dcrbtcvol'] = df['dcrvol'] * df['PriceBTC']
df['dcrbtcvolcum'] = df['dcrbtcvol'].cumsum()
df['wtdcrbtc'] = df['dcrbtcvolcum'] / df['dcrvolcum']
df['ltbtcratio'] = df['PriceBTC'] / df['wtdcrbtc']

#usd metrics
df['dcrusdvol'] = df['dcrvol'] * df['PriceUSD']
df['dcrusdvolcum'] = df['dcrusdvol'].cumsum()
df['wtdcrusd'] = df['dcrusdvolcum'] / df['dcrvolcum']
df['dcrusdvolsum1'] = df['dcrusdvol'].rolling(sum1).sum()
df['dcrusdvolsum2'] = df['dcrusdvol'].rolling(sum2).sum()
df['dcrusdvolsum3'] = df['dcrusdvol'].rolling(sum3).sum()
df['dcrusdvolsum325'] = df['dcrusdvolsum3'] * 0.25

print(df)

""" df.to_excel('vpvr.xlsx') """

# Plot the data
fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

ax1 = plt.subplot(2,1,1)
ax1.plot(df['date'].iloc[:-3], df['PriceBTC'].iloc[:-3], color='w', label='DCRBTC: ' + str(round(df['PriceBTC'].iloc[-4], 5)))
ax1.plot(df['date'].iloc[:-3], df['wtdcrbtc'].iloc[:-3], color='lime', label='LT DCRBTC: ' + str(round(df['wtdcrbtc'].iloc[-3], 5)))
ax1.plot(df['date'].iloc[:-3], df['realdcrbtc'].iloc[:-3], color='aqua', label='Realized DCRBTC: ' + str(round(df['realdcrbtc'].iloc[-4], 5)))
ax1.fill_between(df['date'], df['PriceBTC'], df['realdcrbtc'], where= df['realdcrbtc'] > df['PriceBTC'], facecolor='red', alpha=0.5) 
ax1.fill_between(df['date'], df['PriceBTC'], df['realdcrbtc'], where= df['realdcrbtc'] < df['PriceBTC'], facecolor='lime', alpha=0.5) 
ax1.tick_params(color='w', labelcolor='w')
ax1.set_facecolor('black')
ax1.set_title("DCRBTC & Lifetime Ticket Price", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.grid()
ax1.legend()
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

ax2 = plt.subplot(2,1,2)
line = ax2.plot(df['date'].iloc[:-3], df['PriceUSD'].iloc[:-3], color='w', label='DCRUSD: ' + str(round(df['PriceUSD'].iloc[-4], 2)))
ax2.plot(df['date'].iloc[:-3], df['wtdcrusd'].iloc[:-3], color='lime', label='LT DCRUSD: ' + str(round(df['wtdcrusd'].iloc[-3], 2)))
""" ax2.plot(df['date'].iloc[:-3], df['realdcrusd'].iloc[:-3], color='aqua', label='Realized DCRUSD: ' + str(round(df['realdcrusd'].iloc[-4], 2)))
ax2.fill_between(df['date'], df['PriceUSD'], df['realdcrusd'], where= df['realdcrusd'] > df['PriceUSD'], facecolor='red', alpha=0.5) 
ax2.fill_between(df['date'], df['PriceUSD'], df['realdcrusd'], where= df['realdcrusd'] < df['PriceUSD'], facecolor='lime', alpha=0.5)  """
ax2.tick_params(color='w', labelcolor='w')
ax2.set_facecolor('black')
ax2.set_title("DCRUSD & Lifetime Ticket Price", fontsize=20, fontweight='bold', color='w')
ax2.set_yscale('log')
ax2.grid()
ax2.legend(loc='lower right')
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

""" ax1 = plt.subplot(1,1,1)
ax1.plot(df['date'].iloc[:-2], df['CapMrktCurUSD'].iloc[:-2], color='w', label='Market Cap: ' + str(format(round(df['CapMrktCurUSD'].iloc[-2]),',')))
ax1.plot(df['date'].iloc[:-2], df['dcrusdvolcum'].iloc[:-2], color='lime', label='LT in Tix: ' + str(format(round(df['dcrusdvolcum'].iloc[-2]),',')))
ax1.plot(df['date'].iloc[:-2], df['dcrusdvolsum3'].iloc[:-2], color='aqua', label='142 in Tix: ' + str(format(round(df['dcrusdvolsum3'].iloc[-2]),',')))
ax1.plot(df['date'].iloc[:-2], df['dcrusdvolsum325'].iloc[:-2], color='aqua', label='142 in Tix 25%: ' + str(format(round(df['dcrusdvolsum325'].iloc[-2]),',')))
ax1.tick_params(color='w', labelcolor='w')
ax1.set_facecolor('black')
ax1.set_title("DCRBTC / Lifetime Ticket Price", fontsize=20, fontweight='bold', color='w')
ax1.set_yscale('log')
ax1.grid()
ax1.legend()
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

plt.show()