# GENERAL

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://explorer.dcrdata.org/")

#   TICKET DATA
ob = dcrdata.chart.market.depth("BTC")
print(ob)


