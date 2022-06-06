import pandas as pd
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

price_ratio = 3
impermanent_loss = ((2 * np.sqrt(price_ratio) / (1 + price_ratio)) - 1) #Constant, do not change

print("Impermanent Loss: " + str(impermanent_loss*100) + "%")

lp_roi = .35
lp_returns = 1 + lp_roi + impermanent_loss  #Constant, do not change

print("LP Net Returns: " + str((lp_returns-1)*100) + "%")   #i.e. HODL outperformance on a % basis

lp_principal = 1000
principal_roi = 2
principal_lp_returns = lp_principal * principal_roi * lp_returns    #Constant, do not change
principal_profit = ((principal_lp_returns - lp_principal) / lp_principal) * 100 #Constant, do not change

print("Initial Investment: $" + str(lp_principal))
print("HODL Value: $" + str(lp_principal*principal_roi))
print("Total Value (Principal + Interest): $" + str(principal_lp_returns))
print("Total Profit on Investment (%): " + str(principal_profit) + "%")