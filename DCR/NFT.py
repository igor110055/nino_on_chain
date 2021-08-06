import pandas as pd
import requests

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
    df = pd.DataFrame(response)
    #df.to_csv('nft.csv')
else:
    while offset >= 0:
        offset = offset - limit
        querystring = {"offset":str(offset),"limit":str(limit),"asset_owner":owner}
        response = requests.request("GET", url, params=querystring)
        response = response.json()
        response_list = pd.DataFrame(response)
        merge_list.append(response_list)
    df = pd.concat(merge_list)
    #df.to_csv('nft.csv')

clean_list = []

for item in df['stats']:
    df2 = pd.DataFrame.from_dict(item, orient='index')
    clean_list.append(df2)
    print(df2)

df1 = pd.concat(clean_list,axis=1)

for col in df1.columns:
    df1.columns = df['name']

df1.to_csv('clean_nft.csv')

print(df1)