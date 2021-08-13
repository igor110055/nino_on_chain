import pandas as pd
import requests
import plotly.express as px

""" endpoints = [assets,collections] """    #different endpoints which you plug to end of url

url = "https://api.opensea.io/api/v1/assets"

# Build base dataframe
offset = 0     #takes you to earliest row - api always starts from most recent
limit = 50   #rows in each call
owner = "0x00c71f8c497d8950553fcb874f4a8cf74dc88629"      #filter by owner
order_direction = "desc"    #or "asc"
collection = "animetas"
order_by = "sale_count"

clean_list = []

while True:

    offset += limit
    querystring = {"order_direction":"desc","offset":str(offset),"limit":str(limit),"collection":collection,"order_by":order_by}

    response = requests.request("GET", url, params=querystring)
    response = response.json()
    df1 = pd.DataFrame(response['assets'])
    clean_list.append(df1)
    
