# GENERAL

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

#   TICKET DATA
ticketPrice = dcrdata.chart("ticket-price")

tix_vol = ticketPrice['count']
tix_price = []

for precio in ticketPrice['price']:
    adj_precio = precio / 100000000
    tix_price.append(adj_precio)

tix = pd.DataFrame(tix_vol)
price = pd.DataFrame(tix_price)
dcr_tix = tix * price
tix['ticket prices'] = price
#tix.to_excel('ticket_data.xlsx')
#print(dcr_tix)

sum2 = dcr_tix.rolling(window=2).sum()
max28 = sum2.rolling(window=56).max()
max142 = sum2.rolling(window=284).max()
ratio = max28 / max142
print(max28)

# merge datasets
vol = pd.concat([max28, max142, ratio], axis=1, sort=False)
vol.to_excel('vol analysis.xlsx')

#plot
plt.figure()
ax1 = plt.subplot(3, 1, 1)
plt.plot(max28)
plt.title("Max 28")

plt.subplot(3, 1, 2, sharex=ax1)
plt.plot(max142)
plt.title("Max 142")
plt.yscale('log')

plt.subplot(3, 1, 3, sharex=ax1)
plt.plot(ratio)
plt.title("28 Day / 142 Day Ratio")

plt.show()