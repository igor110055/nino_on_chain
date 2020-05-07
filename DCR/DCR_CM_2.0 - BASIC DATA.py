# THIS CODE WILL HELP KICK OFF WORK ON A NEW MODULE, JUST COPY + PASTE

# Import the API
import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
import pandas as pd

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List the assets Coin Metrics has data for.
supported_assets = cm.get_supported_assets()
print("supported assets:\n", supported_assets)

# List all available metrics for DCR.
asset = "dcr"
available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)




