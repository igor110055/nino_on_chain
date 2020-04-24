from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

#   TICKET DATA
ticketPrice = dcrdata.chart("ticket-price")
print(ticketPrice.keys())
tix_vol = ticketPrice['count']

# Convert to pandas
df = pd.DataFrame(tix_vol)
#print(df)

# Get 7-Day (14 period) rolling average
rolling_7 = df.rolling(window=14).mean()
rolling_28 = df.rolling(window=56).mean()
#print(rolling_7)

# Plot the data
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(rolling_7)
plt.title("7-Day Tix Vol Avg")

plt.subplot(2, 1, 2)
plt.plot(rolling_28)
plt.title("28-Day Tix Vol Avg")
plt.show()