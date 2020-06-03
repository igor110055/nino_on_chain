# COINMETRICS
import coinmetrics
import cm_data_converter as cmdc

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
""" print(df) """

# Pull CM Price Data

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# Pull data
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-06-02"

price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)
mcap = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2)
realcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapRealUSD", date_1, date_2))
realcap['date'] = pd.to_datetime(realcap['date'], utc=True).dt.strftime('%Y-%m-%d')

# Clean CM data

cm_df = cmdc.cm_data_convert(price)
cm_df1 = cmdc.cm_date_format(price)
cm_df2 = cmdc.cm_data_convert(mcap)

cm_df1['DCRUSD'] = cm_df
cm_df1['Market Cap USD'] = cm_df2
cm_df1[0] = pd.to_datetime(cm_df1[0], utc=True).dt.strftime('%Y-%m-%d')
cm_df1.columns = ['date', 'DCRUSD', 'Market Cap USD']

""" print(cm_df1) """

# Merge tixdata and CM data

comb_df = df.merge(cm_df1, on='date', how='left').merge(realcap, on='date', how='left')
comb_df.columns = ['count', 'price', 'date', 'window', 'dcrtixvol', 'DCRUSD', 'Market Cap USD', 'realcap']

# Add columns needed for Strong Hand Calc

comb_df['tixvolusd'] = comb_df['dcrtixvol'] * comb_df['DCRUSD']
comb_df['rollingusdsum'] = comb_df['tixvolusd'].rolling(window=2).sum()
comb_df['max28days'] = comb_df['rollingusdsum'].rolling(window=56).max()
comb_df['max142days'] = comb_df['rollingusdsum'].rolling(window=284).max()
comb_df['28strongcap'] = comb_df['max28days'] * 28
comb_df['142strongcap'] = comb_df['max142days'] * 28
comb_df['28ratio'] = comb_df['Market Cap USD'] / comb_df['28strongcap']
comb_df['142ratio'] = comb_df['Market Cap USD'] / comb_df['142strongcap'] 
comb_df['142 top band'] = comb_df['142strongcap'] * 1.45
comb_df['142 bottom band'] = comb_df['142strongcap'] * 0.6
comb_df['realizedtop'] = comb_df['realcap'] * 2
comb_df['realizedbottom'] = comb_df['realcap'] * 0.5

comb_df.to_excel('stronghand.xlsx')

comb_df['date'] = pd.to_datetime(comb_df['date'])

print(comb_df)

#plot
plt.figure()
ax1 = plt.subplot(2, 1, 1)
plt.plot(comb_df['date'], comb_df['28ratio'], color='r')
plt.axhspan(1.7, 0.9, color='g', alpha=0.25)
plt.title("28 ratio")
plt.grid()
plt.tight_layout()

plt.subplot(2, 1, 2, sharex=ax1)
plt.plot(comb_df['date'], comb_df['Market Cap USD'])
plt.plot(comb_df['date'], comb_df['142 top band'], label='142 Top Band')
plt.plot(comb_df['date'], comb_df['142 bottom band'], label='142 Bottom Band')
plt.plot(comb_df['date'], comb_df['realcap'], label='Realized Cap')
plt.plot(comb_df['date'], comb_df['realizedtop'], label='Realized Top', linestyle=':')
plt.plot(comb_df['date'], comb_df['realizedbottom'], label='Realized Bottom', linestyle=':')
plt.title("Market Cap USD vs 142 Bands vs Realized Cap")
plt.legend()
plt.grid()
plt.tight_layout()
plt.yscale('log')

plt.show()