# COINMETRICS
import coinmetrics
import cm_data_converter as cmdc
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

# EARLY PRICE DATA
filename = 'DCR/DCR_data.xlsx'
df_early = pd.read_excel(filename)
early = df_early[['date', 'PriceUSD', 'PriceBTC', 'CapMrktCurUSD']].copy()
early['date'] = pd.to_datetime(pd.to_datetime(early['date'], utc=True).dt.strftime('%Y-%m-%d'))
early.rename(columns={'PriceUSD': 'dcrusd', 'PriceBTC': 'dcrbtc', 'CapMrktCurUSD': 'dcrmarketcap'}, inplace=True)

# COINMETRICS + MERGE EARLY

cm = coinmetrics.Community()

# Pull data
asset = "dcr"

date_1 = "2016-02-08"
date_2 = "2020-07-07"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
pricebtc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))
mcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))
supply = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "SplyCur", date_1, date_2))
price = supply.merge(price, on='date', how='left').merge(pricebtc, on='date', how='left').merge(mcap, on='date', how='left')
price['date'] = pd.to_datetime(pd.to_datetime(price['date'], unit='s', utc=True).dt.strftime('%Y-%m-%d'))
price.columns = ['date', 'supply', 'PriceUSD', 'PriceBTC', 'mcap']

price = price.merge(early, on='date', how='left')
price = price.fillna(0)

price['PriceUSD'].mask(price['PriceUSD'] == 0, price['dcrusd'], inplace=True, axis=0)
price['PriceBTC'].mask(price['PriceBTC'] == 0, price['dcrbtc'], inplace=True, axis=0)
price['mcap'].mask(price['mcap'] == 0, price['dcrmarketcap'], inplace=True, axis=0)
price = price.drop(columns=['dcrusd', 'dcrusd', 'dcrbtc', 'dcrmarketcap'])

# DCRDATA

df = pd.DataFrame(dcrdata.chart("chainwork"))
df['t'] = pd.to_datetime(pd.to_datetime(df['t'], unit='s', utc=True).dt.strftime('%Y-%m-%d'))
df.rename(columns={'t': 'date'}, inplace=True)
df = df.drop(columns=['axis', 'bin'])

df = df.merge(price, on='date', how='left')

# Calc Metrics

df['addsupp'] = df['supply'].diff(1)
df['addwork'] = df['work'].diff(1)

df['workvalue'] = (df['addsupp'] * df['addwork']) * df['PriceUSD'] 
df['worksupp'] = df['workvalue'].cumsum()
df['workadj'] = df['worksupp'] / df['work']

print(df)

plt.plot(df['date'], df['workadj'])
plt.show()