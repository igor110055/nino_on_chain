import pandas as pd
import requests

""" endpoints = [assets,collections] """    #different endpoints which you plug to end of url

url = "https://api.opensea.io/api/v1/collections"

# Build base dataframe
offset = 50000      #takes you to earliest date in api
limit = 250     #rows in each call
owner = 0x0601d0235645a6ce6356ef11aa0b225c68605131

merge_list = []
while offset > 0:
    offset = offset - limit
    querystring = {"offset":str(offset),"limit":str(limit),"asset_owner":str(owner)}
    response = requests.request("GET", url, params=querystring)
    response = response.json()
    response_list = pd.DataFrame(response['collections'])
    merge_list.append(response_list)
df = pd.concat(merge_list)

df.to_csv('nft.csv')

