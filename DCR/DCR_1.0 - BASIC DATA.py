# GENERAL

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

#   TICKET DATA
ticketPrice = dcrdata.chart("ticket-price")

#print(ticketPrice.values())
print(ticketPrice.keys())
#print(ticketPrice['count'])
tix_vol = ticketPrice['count']
#print(ticketPrice['price'])
tix_price = []

for precio in ticketPrice['price']:
    adj_precio = precio / 100000000
    tix_price.append(adj_precio)

#print(tix_price)
#plt.plot(tix_price)
#plt.show()

# STAKE PARTICIPATION %

Stk_part = dcrdata.chart("stake-participation")
print(Stk_part.keys())
Pool_per = Stk_part['poolval']
Dcr_circ = Stk_part['circulation']
Stake_per = [i / j for i, j in zip(Pool_per, Dcr_circ)]
#plt.plot(Stake_per)
#plt.show()
#print(Stake_per)

# POW DIFFICULTY

Diff_data = dcrdata.chart("pow-difficulty")
print(Diff_data.keys())
Difficulty = Diff_data['diff']
plt.plot(Difficulty)
plt.show()

#   PRIVACY

Privacy_data = dcrdata.chart("privacy-participation")
print(Privacy_data.keys())
anon_set = Privacy_data['anonymitySet']
