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
date_2 = "2020-05-19"

price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)
mcap = cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2)

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

comb_df = df.merge(cm_df1, on='date', how='left')

# Add columns needed for Strong Hand Calc

comb_df['tixvolusd'] = comb_df['dcrtixvol'] * comb_df['DCRUSD']
comb_df['142 SUM'] = comb_df['tixvolusd'].rolling(284, min_periods=1).sum()
comb_df['142 BOTTOM'] = comb_df['142 SUM'] *0.25
comb_df['Lifetime USD in Tickets'] = comb_df['tixvolusd'].cumsum()

print(comb_df)

comb_df.to_excel('142 tix vol.xlsx')

# PLOT

plt.plot(comb_df['Market Cap USD'])
plt.plot(comb_df['142 SUM'], label='142 SUM')
plt.plot(comb_df['142 BOTTOM'], label='142 BOTTOM')
plt.plot(comb_df['Lifetime USD in Tickets'], label='LIFETIME USD IN TIX')
plt.legend()
plt.grid()
plt.yscale('log')
plt.title("Market Cap versus 142 Day Tix Vol Sum")
plt.show()