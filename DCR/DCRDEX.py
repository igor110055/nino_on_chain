import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import numpy as np

response = requests.get("https://explorer.dcrdata.org/api/exchanges/")
response = response.json()
df = pd.DataFrame(response)
df.to_csv('dcrdex.csv')

timeframe = 3       #3 = daily  4 = hourly

#DCRDEX
df1 = pd.DataFrame.from_dict(df['dcr_btc_exchanges'].iloc[2], orient='columns')
df2 = pd.DataFrame.from_dict(df1['candlesticks'].iloc[timeframe], orient='columns')     
df2['start'] = pd.to_datetime(df2['start'], utc=True)
df2['start'] = df2['start'] + datetime.timedelta(seconds=10)

print(df1['candlesticks'])

#BINANCE
df3 = pd.DataFrame.from_dict(df['dcr_btc_exchanges'].iloc[0], orient='columns')
df4 = pd.DataFrame.from_dict(df3['candlesticks'].iloc[timeframe], orient='columns')
df4['start'] = pd.to_datetime(df4['start'])

df4.columns = ['binance_high','binance_low','binance_open','binance_close','binance_volume','start']

print(df4)

#MERGE
df2 = df2.merge(df4, on='start', how='left')

#METRICS
df2['30_day'] = df2['volume'].rolling(30).mean()
df2['cum_vol'] = df2['volume'].cumsum()
df2['btc_vol'] = df2['volume'] * df2['close']

df2['price_diff'] = ((df2['close'] / df2['binance_close']) - 1) * 100
df2['price_diff_pos'] = np.where(df2['price_diff'] >= 0, df2['price_diff'], 0)
df2['price_diff_neg'] = np.where(df2['price_diff'] < 0,  df2['price_diff'], 0)

df2['volume_diff'] = ((df2['volume'] / df2['binance_volume']) - 1) * 100
df2['volume_diff_pos'] = np.where(df2['volume_diff'] >= 0, df2['volume_diff'], 0)
df2['volume_diff_neg'] = np.where(df2['volume_diff'] < 0,  df2['volume_diff'], 0)

print(df2)

#PLOT

#DCRDEX vs Binance Price Premium / Discount

top = 4
bottom = -1

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=df2['start'].iloc[top:bottom], y=df2['close'].iloc[top:bottom], name="DCRBTC Price", line=dict(color="#000000")),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df2['start'].iloc[top:bottom], y=df2['price_diff_pos'].iloc[top:bottom], name="Premium (%)", fill="tozeroy", line=dict(color="#00FF00")),
    secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=df2['start'].iloc[top:bottom], y=df2['price_diff_neg'].iloc[top:bottom], name="Discount (%)", fill="tozeroy", line=dict(color="#FF0000")),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="DCRDEX (1) Price & (2) Premium, & Discount vs Binance Price"
)

# Set x-axis title
fig.update_xaxes(title_text="Date")

# Set y-axes titles
fig.update_yaxes(title_text="Price (BTC)", secondary_y=False)
fig.update_yaxes(title_text="Premium / Discount (%)", secondary_y=True)

fig.show()

#DCRDEX Volume

top1 = 0
bottom1 = -1

fig1 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig1.add_trace(
    go.Scatter(x=df2['start'].iloc[top1:bottom1], y=df2['close'].iloc[top1:bottom1], name="DCRBTC Price", line=dict(color="#000000")),
    secondary_y=False,
)

fig1.add_trace(
    go.Scatter(x=df2['start'].iloc[top1:bottom1], y=df2['volume'].iloc[top1:bottom1], name="Volume (DCR)", fill="tozeroy", line=dict(color="#00FF00")),
    secondary_y=True,
)

# Add figure title
fig1.update_layout(
    title_text="DCRDEX Price vs Volume"
)

# Set x-axis title
fig1.update_xaxes(title_text="Date")

# Set y-axes titles
fig1.update_yaxes(title_text="Price (BTC)", secondary_y=False)
fig1.update_yaxes(title_text="Volume", secondary_y=True)

fig1.show()

#DCRDEX vs Binance Volume

top2 = 2
bottom2 = -1

fig2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig2.add_trace(
    go.Scatter(x=df2['start'].iloc[top2:bottom2], y=df2['close'].iloc[top2:bottom2], name="DCRBTC Price", line=dict(color="#000000")),
    secondary_y=False,
)

fig2.add_trace(
    go.Scatter(x=df2['start'].iloc[top2:bottom2], y=df2['volume_diff_pos'].iloc[top2:bottom2], name="Surplus (%)", fill="tozeroy", line=dict(color="#00FF00")),
    secondary_y=True,
)

fig2.add_trace(
    go.Scatter(x=df2['start'].iloc[top2:bottom2], y=df2['volume_diff_neg'].iloc[top2:bottom2], name="Shortage (%)", fill="tozeroy", line=dict(color="#FF0000")),
    secondary_y=True,
)

# Add figure title
fig2.update_layout(
    title_text="DCRDEX (1) Price & (2) Surplus, & Shortage vs Binance Volume"
)

# Set x-axis title
fig2.update_xaxes(title_text="Date")

# Set y-axes titles
fig2.update_yaxes(title_text="Price (BTC)", secondary_y=False)
fig2.update_yaxes(title_text="Surplus / Shortage (%)", secondary_y=True)

fig2.show()