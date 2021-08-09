import pandas as pd
import requests
import plotly.express as px

""" endpoints = [assets,collections] """    #different endpoints which you plug to end of url

url = "https://api.opensea.io/api/v1/collections"

# Build base dataframe
offset = 0     #takes you to earliest row - api always starts from most recent
limit = 300    #rows in each call
owner = "0x0601d0235645a6ce6356ef11aa0b225c68605131"      #filter by owner

merge_list = []
if offset == 0:
    querystring = {"offset":str(offset),"limit":str(limit),"asset_owner":owner}
    response = requests.request("GET", url, params=querystring)
    response = response.json()
    df2 = pd.DataFrame(response)
    df2.to_csv('nft.csv')
else:
    while offset >= 0:
        offset = offset - limit
        querystring = {"offset":str(offset),"limit":str(limit),"asset_owner":owner}
        response = requests.request("GET", url, params=querystring)
        response = response.json()
        response_list = pd.DataFrame(response)
        merge_list.append(response_list)
    df2 = pd.concat(merge_list)
    df2.to_csv('nft.csv')
print(df2)

clean_list = []

for item in df2['stats']:
    df1 = pd.DataFrame.from_dict(item, orient='index')
    clean_list.append(df1)
    print(df1)

df = pd.concat(clean_list,axis=1)
df = df.transpose()
df.reset_index(inplace=True,drop=True)
df.insert(0, "name", df2['name'])
#df1.to_csv('clean_nft.csv')

print(df)

#Build Metrics

df['seven_day_trade_count'] = df['seven_day_volume'] / df['seven_day_average_price']
df['seven_day_liquidity'] = df['seven_day_trade_count'] / df['total_supply']

#Charting

fig = px.bar(df, x='name', y='seven_day_liquidity', title='Stats for Collections Owned by ' + owner)
fig.show()