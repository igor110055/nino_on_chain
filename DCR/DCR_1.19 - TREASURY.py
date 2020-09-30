import coinmetrics
import cm_data_converter as cmdc

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")
import matplotlib.ticker as ticker
import matplotlib as mpl
import numpy as np

# Add csv

filename = 'DCR/treasury.csv'
df = pd.read_csv(filename)

# Format csv

df = df.drop(columns=['tx_hash', 'io_index', 'valid_mainchain', 'tx_type', 'matching_tx_hash'])
df['time_stamp'] = pd.to_datetime(df['time_stamp'], unit='s').dt.strftime('%Y-%m-%d')
df = df.sort_values(by='time_stamp')
df = df.reset_index()

df['value'] = df['direction'] * df['value']   
df['dcrinflow'] = np.where(df['value'] > 0, df['value'], 0)
df['dcroutflow'] = np.where(df['value'] < 0, df['value'], 0)

# CM data
cm = coinmetrics.Community()
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-09-30"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
mcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))

# Merge treasury and CM data

price = price.merge(mcap, on='date', how='left')
price['date'] = price['date'].dt.strftime('%Y-%m-%d')   # convert date to merge
price.columns = ['time_stamp', 'PriceUSD', 'Mcap']

df1 = pd.DataFrame(df.groupby('time_stamp')['dcroutflow'].sum())    #group outflows and sum
df2 = pd.DataFrame(df.groupby('time_stamp')['dcrinflow'].sum()) #group inflows and sum

df1 = df1.merge(df2, on='time_stamp', how='left')
df1['value'] = df1['dcrinflow'] + df1['dcroutflow'] # net daily outflows and inflows

df1 = df1.merge(price, on='time_stamp', how='left')
df1['time_stamp'] = pd.to_datetime(df1['time_stamp']) # change back to datetime for plotting

# Create metrics

total = 1932000

bull = 0.005
bullish = 0.01
moderate = 0.015
bearish = 0.02
bear = 0.03
doom = 0.04

df1['Price30'] = df1['PriceUSD'].rolling(30).mean()
df1['Price90'] = df1['PriceUSD'].rolling(90).mean()

df1['treasiss'] = df1['dcrinflow'].cumsum()
df1['treasrem'] = total - df1['treasiss']

df1['dcroutflowmax'] = (df1['dcroutflow'].rolling(90).min()) * -1
df1['dcrtotoutflow'] = df1['dcroutflow'].cumsum() * -1
df1['adjdcroutflow'] = df1['dcroutflow'] * -1

df1['usdoutflow'] = df1['dcroutflow'] * df1['PriceUSD']
df1['adjusdoutflow'] = df1['usdoutflow'] * -1
df1['usdoutflowcont'] = df1['dcroutflow'] * df1['Price30']
df1['usdoutflowmax'] = (df1['usdoutflow'].rolling(90).min()) * -1
df1['cumoutusd'] = (df1['usdoutflow'].cumsum()) * -1
df1['40drawdown'] = df1['cumoutusd'] * 0.6
df1['contractearnings'] = ((-1 * df1['dcroutflow'].cumsum() * df1['PriceUSD']))

df1['monthflow'] = df1['value'].rolling(90).sum()
df1['treasury'] = df1['value'].cumsum()
df1['valueusd'] = df1['value'] * df1['PriceUSD']
df1['treasuryusd'] = df1['treasury'] * df1['PriceUSD']
df1['projrem'] = df1['treasury'] + df1['treasrem']
df1['valperdcr'] = df1['Mcap'] / df1['treasury']
df1['contractpl'] = df1['usdoutflowcont'] - df1['usdoutflow'] 
df1['qtrcontractpl'] = ((df1['dcroutflow'].rolling(90).sum() * df1['PriceUSD']) - df1['usdoutflow'].rolling(90).sum()) / df1['usdoutflow'].rolling(90).sum()
df1['qtrcontractplusd'] = ((-1 * df1['dcroutflow'].rolling(365, min_periods=1).sum() * df1['PriceUSD']) + df1['usdoutflow'].rolling(365, min_periods=1).sum())
df1['ltcontractplusd'] = ((-1 * df1['dcroutflow'].cumsum() * df1['PriceUSD']) + df1['usdoutflow'].cumsum()) / (-1 * df1['usdoutflow'].cumsum())

df1['wtoutflow'] = df1['dcroutflow'] / df1['treasury']
df1['wtlow'] = df1['wtoutflow'].rolling(90).min()
df1['adjwtlow'] = df1['wtlow'] * -1

df1['bullprice'] = df1['Price90'] * (df1['adjwtlow'] / bull)
df1['bullishprice'] = df1['Price90'] * (df1['adjwtlow'] / bullish)
df1['moderateprice'] = df1['Price90'] * (df1['adjwtlow'] / moderate)
df1['bearishprice'] = df1['Price90'] * (df1['adjwtlow'] / bearish)
df1['bearprice'] = df1['Price90'] * (df1['adjwtlow'] / bear)
df1['doomprice'] = df1['Price90'] * (df1['adjwtlow'] / doom)

df1['bulltreasury'] = df1['treasury'] * df1['bullprice']
df1['runway'] = df1['projrem'] / df1['dcroutflowmax']
df1['PE'] = df1['treasuryusd'] / df1['cumoutusd']
df1['equity'] = df1['treasuryusd'] - df1['cumoutusd']

df1['pe2'] = 2 * df1['cumoutusd']
df1['pe5'] = 5 * df1['cumoutusd']
df1['pe10'] = 10 * df1['cumoutusd']
df1['pe20'] = 20 * df1['cumoutusd']
df1['pe40'] = 40 * df1['cumoutusd']
df1['pe60'] = 60 * df1['cumoutusd']

print(df1)
df1.to_csv('treas.csv')

# Plot

fig, ax1 = plt.subplots()
fig.patch.set_facecolor('black')
fig.patch.set_alpha(1)

""" ax1 = plt.subplot(2,1,1)
ax1.plot(df1['time_stamp'], df1['PriceUSD'], color='w', label='DCRUSD')
ax1.plot(df1['time_stamp'], df1['bullprice'], color='lime', alpha=0.75, label='0.5% Treasury Spend')
ax1.plot(df1['time_stamp'], df1['bullishprice'], color='g', alpha=0.75, label='1% Treasury Spend')
ax1.plot(df1['time_stamp'], df1['moderateprice'], color='orange', alpha=0.75, label='1.5% Treasury Spend')
ax1.plot(df1['time_stamp'], df1['bearishprice'], color='pink', alpha=0.75, label='2% Treasury Spend')
ax1.plot(df1['time_stamp'], df1['bearprice'], color='m', alpha=0.75, label='3% Treasury Spend')
ax1.plot(df1['time_stamp'], df1['doomprice'], color='r', alpha=0.75, label='4% Treasury Spend')
ax1.set_ylabel('USD Price', fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.set_yscale('log')
ax1.set_title("DCRUSD vs Budget Prices", fontsize=20, fontweight='bold', color='w')
ax1.set_facecolor('black')
ax1.grid()
ax1.legend(loc='upper left')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax11 = plt.subplot(2,1,2, sharex=ax1)
ax11.bar(df1['time_stamp'], df1['adjwtlow'], color='w')
ax11.tick_params(color='w', labelcolor='w')
ax11.set_title("% of Treasury Spent on Contractor Paydays (90 Day Max)", fontsize=20, fontweight='bold', color='w')
ax11.set_facecolor('black')
ax11.set_ylabel('% Spent', fontsize=20, fontweight='bold', color='w')
ax11.axhline(0.02, color='aqua', linestyle='dashed')
ax11.grid() """


ax1 = plt.subplot(1,1,1)
ax1.plot(df1['time_stamp'], df1['treasuryusd'], color='w', alpha=1, label='Treasury USD Balance')
ax1.set_facecolor('black')
ax1.set_title("Treasury USD Balance vs Treasury Runway", fontsize=20, fontweight='bold', color='w')
ax1.set_ylabel('Treasury Balance USD', fontsize=20, fontweight='bold', color='w')
ax1.tick_params(color='w', labelcolor='w')
ax1.legend(loc='upper left')
ax1.set_yscale('log')
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

ax11 = ax1.twinx()
""" ax11.bar(df1['time_stamp'], df1['runway'], color='aqua', alpha=0.5) """
ax11.fill_between(df1['time_stamp'], df1['monthflow'], where= df1['monthflow'] > 0, facecolor='aqua', alpha=1) 
ax11.fill_between(df1['time_stamp'], df1['monthflow'], where= df1['monthflow'] < 0, facecolor='red', alpha=0.7) 
ax11.grid()
ax11.set_ylabel('Months of Treasury Runway', fontsize=20, fontweight='bold', color='w')
ax11.tick_params(color='w', labelcolor='w')
ax11.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))


""" ax2 = plt.subplot(1,1,1, sharex=ax1)
ax2.plot(df1['time_stamp'], df1['contractearnings'], label='Treasury USD Value', color='w')
ax2.plot(df1['time_stamp'], df1['cumoutusd'], label='Total Contractor USD Pay', color='aqua')
ax2.plot(df1['time_stamp'], df1['40drawdown'], label='Earnings 40% Drawdown', color='red')
ax2.plot(df1['time_stamp'], df1['pe2'], label='2x')
ax2.plot(df1['time_stamp'], df1['pe5'], label='5x')
ax2.plot(df1['time_stamp'], df1['pe10'], label='10x')
ax2.plot(df1['time_stamp'], df1['pe20'], label='20x')
ax2.plot(df1['time_stamp'], df1['pe40'], label='40x')
ax2.plot(df1['time_stamp'], df1['pe60'], label='60x')
ax2.fill_between(df1['time_stamp'], df1['pe10'], df1['pe20'], where= df1['pe20'] > df1['pe10'], facecolor='lime', alpha=0.7)
ax2.grid()
ax2.set_facecolor('black')
ax2.set_title("Valuation of Treasury vs Multiples of Contracting Pay", fontsize=20, fontweight='bold', color='w')
ax2.tick_params(color='w', labelcolor='w')
ax2.set_ylabel("USD Value", fontsize=20, fontweight='bold', color='w')
ax2.set_yscale('log')
ax2.legend(loc='upper left')
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

""" ax22 = ax2.twinx()
ax22.plot(df1['time_stamp'], df1['ltcontractplusd'], color='red', alpha=0.3)
ax22.tick_params(color='w', labelcolor='w')
ax22.set_ylim((-1.3, 18))
ax22.grid()
ax22.fill_between(df1['time_stamp'], df1['ltcontractplusd'], where=df1['ltcontractplusd'] > 0, facecolor='aqua', alpha=0.7)
ax22.fill_between(df1['time_stamp'], df1['ltcontractplusd'], where=df1['ltcontractplusd'] < 0, facecolor='red', alpha=0.7)
ax22.set_yscale('log')
ax22.set_ylabel("Contractor % P/L", fontsize=20, fontweight='bold', color='w')
ax22.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

""" ax22 = ax2.twinx()
ax22.bar(df1['time_stamp'], df1['dcrtotoutflow'], color='pink', alpha=0.5)
ax22.tick_params(color='w', labelcolor='w')
ax22.grid()
ax22.set_ylabel("Max $ Spend (90 Days Rolling)", fontsize=14, fontweight='bold', color='w')
ax22.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

""" ax22 = ax2.twinx()
ax22.plot(df1['time_stamp'], df1['PE'], color='aqua', alpha=1)
ax22.tick_params(color='w', labelcolor='w')
ax22.grid()
ax22.set_ylabel("Treasury Value / Cum. Treasury Spend", fontsize=14, fontweight='bold', color='w')
ax22.set_yscale('log')
ax22.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) """

plt.show()