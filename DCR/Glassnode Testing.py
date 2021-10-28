from glassnode_api_python_client.glassnode import GlassnodeClient
import pandas as pd
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

gn = GlassnodeClient()
interval = '1h'
period = 336
list_end = -1

mcap = gn.get(
    'https://api.glassnode.com/v1/metrics/market/marketcap_usd',
    a='BTC',
    s='2021-01-01',
    i=interval
)

rcap = gn.get(
    'https://api.glassnode.com/v1/metrics/market/marketcap_realized_usd',
    a='BTC',
    s='2021-01-01',
    i=interval
)

price = gn.get(
    'https://api.glassnode.com/v1/metrics/market/price_usd_close',
    a='BTC',
    s='2021-01-01',
    i=interval
)

df = pd.concat([mcap,rcap,price],axis=1)
df = df.fillna(0)
df.reset_index(level=0, inplace=True)
df.columns = ['date','mcap','rcap','price']

""" METRICS """

df['mcap_change'] = ((
            df['mcap'] 
            - df['mcap'].shift(periods=period,axis=0)
        ) / period)
df['rcap_change'] = ((
            df['rcap'] 
            - df['rcap'].shift(periods=period,axis=0)
        ) / period)
df['change'] = df['mcap_change'] - df['rcap_change']
df['change_norm'] = (df['change'] - df['change'].expanding().mean())/df['change'].expanding().std()
df['change_pos'] = np.where(df['change_norm'] >= 0, df['change_norm'], 0)
df['change_neg'] = np.where(df['change_norm'] < 0,  df['change_norm'], 0)

df['price_change'] = df['price'].diff(1)

df['returns'] = np.where(df['change'] >= 0, df['price_change'], 0)
df['ROI'] = df['returns'].cumsum()

print(df.iloc[:list_end])
print(df['ROI'])

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=df['date'].iloc[:list_end], y=df['mcap'].iloc[:list_end], name="Market Cap"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df['date'].iloc[:list_end], y=df['change_pos'].iloc[:list_end], name="Mkt Real Change Positive", fill="tozeroy"),
    secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=df['date'].iloc[:list_end], y=df['change_neg'].iloc[:list_end], name="Mkt Real Change Negative", fill="tozeroy"),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="Market Cap Change vs Realized Cap Change: " + str(period) + " Days"
)

# Set x-axis title
fig.update_xaxes(title_text="Date")

# Set y-axes titles
fig.update_yaxes(title_text="Market Cap ($)", secondary_y=False)
fig.update_yaxes(title_text="Gradient", secondary_y=True)

fig.show()