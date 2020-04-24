from tinydecred.pydecred.dcrdata import DcrdataClient
from matplotlib import pyplot as plt
import pandas as pd
dcrdata = DcrdataClient("https://alpha.dcrdata.org/")

#   TICKET DATA
total_work = dcrdata.chart("chainwork")
print(total_work.keys())
life_work = total_work['work']

blk_size = dcrdata.chart("blockchain-size")
print(blk_size.keys())
life_size = blk_size['size']

# Convert to pandas
df = pd.DataFrame(life_work)
df_1 = pd.DataFrame(life_size)

# Divide datasets
ratio = df / df_1

plt.plot(ratio)
plt.title("Total Work / Blockchain Size")
plt.yscale('log')
plt.show()