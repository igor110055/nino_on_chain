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
#df.to_excel('duration.xlsx', sheet_name='sup')
# get average
df_sum63 = df.rolling(window=63).sum()
new_sum = df_sum63 - (63*300)
# add time to dataframe and print to check that it worked
new_sum['Time'] = df_1
print(new_sum)
# plot
plt.plot(new_sum['Time'], new_sum[0])
plt.title("Duration Between Blocks (Unit = Seconds)")
plt.show()