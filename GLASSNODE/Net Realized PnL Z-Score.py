from glassnode_api_python_client.glassnode import GlassnodeClient
import pandas as pd
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

gn = GlassnodeClient()
interval = '24h'
period = 155
period1 = 4
list_end = -1

pnl = gn.get(
    'https://api.glassnode.com/v1/metrics/indicators/sopr_less_155',
    a='BTC',
    s='2020-01-01',
    i=interval
)

price = gn.get(
    'https://api.glassnode.com/v1/metrics/market/price_usd_close',
    a='BTC',
    s='2020-01-01',
    i=interval
)

df = pd.concat([pnl,price],axis=1)
df = df.fillna(0)
df.reset_index(level=0, inplace=True)
df.columns = ['date','pnl','price']

""" METRICS """

df['pnl_sum'] = df['pnl'].rolling(period1).sum()
df['pnl_zscore'] = (df['pnl'] - df['pnl'].rolling(period,min_periods=1).mean()) / df['pnl'].rolling(period,min_periods=1).std()
df['pnl_sum_zscore'] = (df['pnl_sum'] - df['pnl_sum'].rolling(period,min_periods=1).mean()) / df['pnl_sum'].rolling(period,min_periods=1).std()

""" CHART """

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=df['date'].iloc[:list_end], y=df['price'].iloc[:list_end], name="Market Cap"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df['date'].iloc[:list_end], y=df['pnl_zscore'].iloc[:list_end], name="SOPR Z-Score", fill="none", line=dict(color="#00FF00")),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="SOPR Z-Score: " + str(period) + " Days"
)

# Set x-axis title
fig.update_xaxes(title_text="Date")

# Set y-axes titles
fig.update_yaxes(title_text="Price ($)", secondary_y=False, type="log")
fig.update_yaxes(title_text="Z-Score", secondary_y=True)

fig.show()