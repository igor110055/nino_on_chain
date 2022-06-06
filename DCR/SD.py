import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import numpy as np
from tinydecred.pydecred.dcrdata import DcrdataClient
from binance.client import Client
import coinmetrics
import cm_data_converter as cmdc
from PIL import Image
import os
import base64

#cm = coinmetrics.Community()

# Pull CM data
""" asset = "dcr"

date_1 = "2010-02-08"
date_2 = "2021-12-30"

dcrbtc = cmdc.combo_convert(cm.get_asset_data_for_time_range(asset, "PriceBTC", date_1, date_2))
dcrbtc.columns = ['start', 'PriceBTC'] """

#DCRDATA

client = DcrdataClient("https://explorer.dcrdata.org/")
df = pd.DataFrame(client.chart("stake-participation"))
df = df.drop(columns=['axis', 'bin'])
df['t'] = pd.to_datetime(df['t'], unit='s')
df['poolval'] = df['poolval'] / 100000000
df['circulation'] = df['circulation'] / 100000000
df.columns = ['circulation','poolval','start']

""" #BINANCE PRICE
asset1 = 'DCRBTC'
dff = pd.DataFrame(Client().get_historical_klines(asset1, Client.KLINE_INTERVAL_1DAY, "8 Feb, 2016", '30 Dec, 2021'))
dff.columns = ['start', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
dff['start'] = pd.to_datetime(dff['start'], unit='ms')    #format date
dff['Open'] = pd.to_numeric(dff['Open'])

#MERGE
df = df.merge(dff,on='start',how='left') """
#df = pd.concat([df,dcrbtc],axis=0)

#METRICS
period = 30
min_rew_param = 0.1
stk_rew_param = 0.8
avg = 14

df['min_rew'] = df['circulation'] * min_rew_param
df['stk_rew'] = df['circulation'] * stk_rew_param

df['pool_chg'] = df['poolval'].diff(period)
df['min_chg'] = df['min_rew'].diff(period) #/ period
df['stk_chg'] = df['stk_rew'].diff(period)

df['demand_chg'] = (df['pool_chg'] - df['stk_chg']) #/ period
df['demand_avg'] = df['demand_chg'].rolling(avg).mean()

df['supply_demand'] = df['demand_chg'] - df['min_chg']

print(df)

#PLOT

fig = go.Figure()

""" fig.add_trace(
    go.Scatter(x=df['start'], y=df['Close'], name="DCRBTC Price", fill="none", line=dict(color="#000000")),
    secondary_y=False,
) """

fig.add_trace(
    go.Scatter(x=df['start'], y=df['supply_demand'], name="Supply_Demand", fill="tozeroy", line=dict(color="#FF0000"))
)

""" fig.add_trace(
    go.Scatter(x=df['start'], y=df['demand_avg'], name="Supply_Demand", fill="none", line=dict(color="#0000FF")),
    secondary_y=True,
) """

# Set x-axis title
fig.update_xaxes(title_text="Date")

# Set y-axes titles
#fig.update_yaxes(title_text="Price (BTC)", secondary_y=False, showgrid=False)
fig.update_yaxes(title_text="DCR Surplus / Deficit", showgrid=False)

# Add images


# Add figure title
fig.update_layout(
    title_text="Supply / Demand for DCR Model assuming " + str(min_rew_param) + " Mining Reward Distribution and " + str(stk_rew_param) + " Staking Rewards Dumping from Surpressor"
)

# Set templates
fig.update_layout(template="plotly_white")

fig.show()

