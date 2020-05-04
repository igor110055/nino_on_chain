from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

#   TICKET DATA
duration = dcrdata.chart("duration-btw-blocks")
print(duration.keys())
print(duration['axis'])
duration_data = duration['duration']
duration_time = duration['t']

# convert to pandas
df = pd.DataFrame(duration_data)
df_1 = pd.DataFrame(duration_time)

# get average
df_avg63 = df.rolling(window=63).mean()
new_avg = df_avg63 - (300)

# add time to dataframe and print to check that it worked
new_avg['Time'] = df_1
new_avg['Raw'] = df
print(new_avg)

# send to excel 
#df.to_excel('duration.xlsx', sheet_name='data')

# plot
plt.plot(new_avg['Time'], new_avg[0])
plt.title("Duration Between Blocks (Unit = Seconds)")
plt.show()