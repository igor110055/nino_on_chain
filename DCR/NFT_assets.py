import pandas as pd
import requests
import plotly.express as px

""" COLLECTIONS """

""" endpoints = [assets,collections] """    #different endpoints which you plug to end of url

url = "https://api.opensea.io/api/v1/collections"

# Build base dataframe
offset = 0     #takes you to earliest row - api always starts from most recent
limit = 300    #rows in each call
owner = "0x3fdbeedcbfd67cbc00fc169fcf557f77ea4ad4ed"      #filter by owner

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
df['slug'] = df2['slug']        #Add slug
df.to_csv('clean_nft.csv')

print(df)

""" ASSETS """

#df.set_index('name')
data_limit = df.loc[62,'total_supply']      #cross reference total supply of a given collection name

url_assets = "https://api.opensea.io/api/v1/assets"

# Build base dataframe
offset_assets = 0     #takes you to earliest row - api always starts from most recent
limit_assets = 50   #rows in each call
owner_assets = "0x3fdbeedcbfd67cbc00fc169fcf557f77ea4ad4ed"      #filter by owner
order_direction_assets = "desc"    #or "asc"
collection_assets = "cryptopunks"       
order_by_assets = "token_id"

clean_list_assets = []

while data_limit > offset_assets:

    offset_assets += limit_assets
    querystring_assets = {"order_direction":"desc","offset":str(offset_assets),"limit":str(limit_assets),"collection":collection_assets,"order_by":order_by_assets}

    response_assets = requests.request("GET", url_assets, params=querystring_assets)
    response_assets = response_assets.json()
    df1_assets = pd.DataFrame(response_assets['assets'])
    clean_list_assets.append(df1_assets)
    print(df1_assets)

df_assets = pd.concat(clean_list_assets)
df_assets.reset_index(inplace=True,drop=True)
df_assets.to_csv('nft_assets.csv')
print(df_assets)

clean_list_traits = []

for item in df_assets['traits']:
   df1_traits = pd.DataFrame(item)
   df1_traits[collection_assets+" ID"] = df_assets.loc[df_assets.index,'token_id']
   print(df1_traits)
   clean_list_traits.append(df1_traits)

df_traits = pd.concat(clean_list_traits)
df_traits.to_csv('nft_traits.csv')
print(df_traits)
    
fig = px.bar(df_assets.head(n=50), x='token_id', y='num_sales', title='Stats for Collections Owned by ' + owner_assets, log_y=False, color='num_sales',
labels={'token_id':collection_assets + ' ID', 'num_sales':'Total Sales for Item'})
fig.show() 

fig1 = px.scatter(df_assets, x='token_id', y='num_sales', title='Stats for Collections Owned by ' + owner_assets, log_y=False, color='num_sales',
labels={'token_id':collection_assets + ' ID', 'num_sales':'Total Sales for Item'})
fig1.show() 