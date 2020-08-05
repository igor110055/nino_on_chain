import coinmetrics
import cm_data_converter as cmdc

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")
import matplotlib.ticker as ticker

# Add csv

filename = 'DCR/treasury.csv'
df = pd.read_csv(filename)

# Format csv

df = df.drop(columns=['tx_hash', 'io_index', 'valid_mainchain', 'tx_type', 'matching_tx_hash'])
df['time_stamp'] = pd.to_datetime(df['time_stamp'], unit='s').dt.strftime('%Y-%m-%d')
df = df.sort_values(by='time_stamp')
df = df.reset_index()

df['dcrflow'] = df['direction'] * df['value']   
df['treasury'] = df['dcrflow'].cumsum()


# CM data
cm = coinmetrics.Community()
asset = "dcr"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)

date_1 = "2016-02-08"
date_2 = "2020-08-04"

price = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2))
mcap = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "CapMrktCurUSD", date_1, date_2))

# Merge treasury and CM data

price = price.merge(mcap, on='date', how='left')
price['date'] = price['date'].dt.strftime('%Y-%m-%d')   # convert date to merge
price.columns = ['time_stamp', 'PriceUSD', 'Mcap']
df = df.merge(price, on='time_stamp', how='left')
df['time_stamp'] = pd.to_datetime(df['time_stamp']) # change back to datetime for plotting

# Create metrics

df['treasuryusd'] = df['treasury'] * df['PriceUSD']
df['dcrflowusd'] = df['dcrflow'] * df['PriceUSD']

print(df)

# Plot

