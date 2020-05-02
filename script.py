import requests
import json
response = requests.get('https://dm-devci-annunciator-services.azurewebsites.net/api/Message/message/0/current')
data = response.json()
print(data['slides'][0]['lines'][0]['content'])
