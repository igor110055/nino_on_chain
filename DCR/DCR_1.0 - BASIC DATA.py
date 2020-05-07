# GENERAL

from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
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

tix = pd.DataFrame(tix_vol)
price = pd.DataFrame(tix_price)

tix['ticket prices'] = price
#tix.to_excel('ticket_data.xlsx')

#print(tix_price)
#plt.plot(tix_price)
#plt.show()

# STAKE PARTICIPATION %

Stk_part = dcrdata.chart("stake-participation")
print(Stk_part.keys())
Pool_per = Stk_part['poolval']
Dcr_circ = Stk_part['circulation']

pool_panda = pd.DataFrame(Pool_per)
circ_panda = pd.DataFrame(Dcr_circ)

adj_pool_panda = pool_panda / 100000000
adj_circ_panda = circ_panda / 100000000
adj_pool_panda['circulation'] = adj_circ_panda

adj_pool_panda.to_excel('stake pool.xlsx')

#plt.plot(Stake_per)
#plt.show()
#print(Stake_per)

# POW DIFFICULTY

Diff_data = dcrdata.chart("pow-difficulty")
print(Diff_data.keys())
Difficulty = Diff_data['diff']
#plt.plot(Difficulty)
#plt.show()

#   PRIVACY

Privacy_data = dcrdata.chart("privacy-participation")
print(Privacy_data.keys())
anon_set = Privacy_data['anonymitySet']

# HASHRATE
Hash_data = dcrdata.chart("hashrate")
print(Hash_data.keys())
hashrate = Hash_data['rate']

# Block Sizes
Block_size = dcrdata.chart("block-size")
print(Block_size.keys())
blocks = Block_size['size']

# Merge Hashrate and Block Size
df = pd.DataFrame(hashrate)
df_1 = pd.DataFrame(blocks)
ratio = df / df_1
ratio_365 = ratio.rolling(window=365).mean()
final_ratio = ratio / ratio_365

