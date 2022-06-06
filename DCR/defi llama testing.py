import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
import numpy as np
from binance.client import Client

#BINANCE
asset = 'CRVUSDT'

date = '10 Sep, 2019'
date1 = '30 Dec, 2022'

df1 = pd.DataFrame(Client().get_historical_klines(asset, Client.KLINE_INTERVAL_1DAY, date, date1))
df1.columns = ['date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']

df1['date'] = pd.to_datetime(df1['date'], unit='ms')    #format date
df1['Open'] = pd.to_numeric(df1['Open'])

#DEFI LLAMA

asset1 = 'curve'

protocols = requests.get("https://api.llama.fi/protocols")
protocols = protocols.json()
#print(protocols)

response = requests.get("https://api.llama.fi/protocol/" + asset1)
response = response.json()
print(response.keys())
df = pd.DataFrame(response['tvl'])
df['date'] = pd.to_datetime(df['date'], unit='s')
print(df)

#MERGE
df['date'] = df['date'].dt.date
df1['date'] = df1['date'].dt.date

df = df.merge(df1, on='date', how='left')
print(df)

df.to_csv('defillama.csv') 

#METRICS

period = 1
df['chg_tvl' + str(period)] = df['totalLiquidityUSD'].diff(periods=period)
df['chg_tvl_pos'] = np.where(df['chg_tvl' + str(period)] >= 0, df['chg_tvl' + str(period)], 0)
df['chg_tvl_neg'] = np.where(df['chg_tvl' + str(period)] < 0,  df['chg_tvl' + str(period)], 0)

#PLOT

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=df['date'], y=df['Close'], name="Price (USD)", line=dict(color="#000000")),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df['date'], y=df['chg_tvl_pos'], name="TVL + (USD)", fill="tozeroy", line=dict(color="#00FF00")),
    secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=df['date'], y=df['chg_tvl_neg'], name="TVL - (USD)", fill="tozeroy", line=dict(color="#FF0000")),
    secondary_y=True,
)


# Add figure title
fig.update_layout(
    title_text= asset1 + " Total Value Locked"
)

# Set x-axis title
fig.update_xaxes(title_text="Date")

# Set y-axes titles
fig.update_yaxes(title_text="Price (USD)", secondary_y=False, type="log")
fig.update_yaxes(title_text="Total Value Locked (USD)", secondary_y=True, type="linear")

fig.show()
