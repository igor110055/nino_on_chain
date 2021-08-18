import pandas as pd
import requests
import plotly.express as px

""" COLLECTIONS """

""" endpoints = [assets,collections] """    #different endpoints which you plug to end of url

url = "https://api.opensea.io/api/v1/collections"

# Build base dataframe
offset = 0     #takes you to earliest row - api always starts from most recent
limit = 300    #rows in each call
owner = "0xe5545c0e1b2dcfcd7c713877ceb6f897705ed62a"      #filter by owner

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
df.to_csv('clean_nft.csv')

print(df)

""" ASSETS """

url_assets = "https://api.opensea.io/api/v1/assets"

# Build base dataframe
offset_assets = 0     #takes you to earliest row - api always starts from most recent
limit_assets = 50   #rows in each call
owner_assets = "0xe5545c0e1b2dcfcd7c713877ceb6f897705ed62a"      #filter by owner
order_direction_assets = "desc"    #or "asc"
collection_assets = "cryptopunks"
order_by_assets = "sale_count"

clean_list_assets = []

while True:

    offset_assets += limit_assets
    querystring_assets = {"order_direction":"desc","offset":str(offset_assets),"limit":str(limit_assets),"collection":collection_assets,"order_by":order_by_assets}

    response_assets = requests.request("GET", url_assets, params=querystring_assets)
    response_assets = response_assets.json()
    df1_assets = pd.DataFrame(response_assets['assets'])
    clean_list_assets.append(df1_assets)
    print(df1_assets)

    if limit_assets > len(response_assets['assets']):
        break

df_assets = pd.concat(clean_list_assets)
df_assets.reset_index(inplace=True,drop=True)
print(df_assets)
    
fig = px.bar(df_assets.head(n=100), x='token_id', y='num_sales', title='Stats for Collections Owned by ' + owner_assets, log_y=False, color='num_sales',
labels={'token_id':'CryptoPunk ID', 'num_sales':'Total Sales for Item'}, barmode='group')
fig.show() 