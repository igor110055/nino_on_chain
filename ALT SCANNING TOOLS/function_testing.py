import coinmetrics
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pandas as pd
import cm_data_converter as cmdc


# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# List all available metrics for DCR.
asset = "btc"

available_data_types = cm.get_available_data_types_for_asset(asset)
print("available data types:\n", available_data_types)
#Fetch data
date_1 = "2016-01-01"
date_2 = "2020-05-09"
price = cm.get_asset_data_for_time_range(asset, "PriceUSD", date_1, date_2)

df = pd.DataFrame(price)
print(df)

""" new_price_value = cmdc.cm_data_convert(price)
new_price_date = cmdc.cm_date_format(price)

new_price_value['date'] = new_price_date

print(new_price_value['date'])
 """
#new_price_value.to_excel('price data.xlsx')

#plt.plot(new_price_value['date'], new_price_value[0])
#plt.show()

