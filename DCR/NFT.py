import pandas as pd
import requests
import plotly.express as px

""" endpoints = [assets,collections] """    #different endpoints which you plug to end of url

url = "https://api.opensea.io/api/v1/collections"

# Build base dataframe
offset = 0     #takes you to earliest row - api always starts from most recent
limit = 300    #rows in each call
owner = "0x00c71f8c497d8950553fcb874f4a8cf74dc88629"      #filter by owner

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

df['nft_wealth'] = df['total_supply'] / df['num_owners']
df['avg_volume'] = df['seven_day_volume'] / 7

df['one_day_eth_wealth'] = df['nft_wealth'] * df['one_day_average_price']
df['one_day_adjeth_wealth'] = df['one_day_eth_wealth'] / df['avg_volume']       #how many days it would take to offload whole NFT stash for a collection

df['seven_day_eth_wealth'] = df['nft_wealth'] * df['seven_day_average_price']
df['seven_day_sales_ratio'] = (df['seven_day_sales'] / df['thirty_day_sales']) / 0.23333

df['thirty_day_price_ratio'] = df['one_day_average_price'] / df['thirty_day_average_price']

#Charting

for col in df.columns:

    fig = px.bar(df, x='name', y=col, title='Stats for Collections Owned by ' + owner, log_y=True, color=col)
    fig.show()

""" fig = px.bar(df, x='name', y='seven_day_sales_ratio', title='Stats for Collections Owned by ' + owner, log_y=False, color='seven_day_sales_ratio',
labels={'name':'Collection Name', 'seven_day_sales_ratio':'7-Day Sales / 30-Day Sales'})
fig.show() """