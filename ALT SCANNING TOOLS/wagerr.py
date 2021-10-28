import requests
import pandas as pd

response = requests.get("https://explorer.wagerr.com/api/bet/results?")
response = response.json()
print(pd.DataFrame(response))




df = pd.DataFrame(response['results'])
df.to_csv('wagergetbetresults.csv')