from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

#   TICKET DATA
ticketPrice = dcrdata.chart("ticket-price")
print(ticketPrice.keys())
tix_vol = ticketPrice['count']

tix_price = []

for precio in ticketPrice['price']:
    adj_precio = precio / 100000000
    tix_price.append(adj_precio)

# Convert to pandas
df = pd.DataFrame(tix_vol)
df_1 = pd.DataFrame(tix_price)

# Calculate DCR in tix per window
df_2 = df * df_1

# Calculate 28 and 56 day sum of dcr in tix, then divide them to get chop ratio for tix

chop_28 = df_2.rolling(window=56).sum()
chop_56 = df_2.rolling(window=112).sum()
chop_142 = df_2.rolling(window=284).sum()

chop_ratio = chop_28 / chop_56
chop_ratio_1 = chop_28 / chop_142

# Plot the data
plt.figure()
plt.subplot(1, 1, 1)
plt.plot(chop_ratio)
plt.title("28/56")

'''plt.subplot(2, 1, 2)
plt.plot(chop_ratio_1)
plt.title("28/142")'''
plt.show()
