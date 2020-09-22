# basic imports
import requests
import pandas as pd

# COINMETRICS
import coinmetrics
import cm_data_converter as cmdc
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter
from binance.client import Client

# api connect

api_key = 'ULgUTHU0vZODL2q4FmTHArsVy1iTJoDaqIMwSThKMKR7wvWZnDO2a2pxvVW9UEph'
api_secret = 'Jq2r0tvBv7QFEE72DObbWpRlvmSmJQIeSzFm4oAKNx3AW8mSOL17CM2wLt9yr0WU'

client = Client(api_key, api_secret)

# pull data
coin = 'DCRBTC'

df = client.get_order_book(symbol=coin)

print(df)