import requests
import json

f = open("modelname.txt", "r")
x = ""

for line in f:
  stripped_line = line.rstrip()
  x += stripped_line
f.close()

# Configure the below URL with the route to your rasa-x api/auth
import os
rasa_url = os.getenv('RASA_URL', 'https://<rasa-x route>')
url = f'{rasa_url}/api/auth'
headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache'}
# Configure the below payload to your rasa-x username and password
rasa_username = os.getenv('RASA_USERNAME', 'me')
rasa_password = os.getenv('RASA_PASSWORD', 'rasaxpassword')
payload = f'{{"username": "{rasa_username}", "password": "{rasa_password}"}}'

r = requests.post(url, data=payload, headers=headers, verify=False)
binary = r.content
output = json.loads(binary)
auth = output['access_token']
print(auth)

url = f"{rasa_url}/api/projects/default/models/{x}/tags/production"

payload = ""
headers = {
    'Authorization': "Bearer " + auth,
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }

f = open( 'auth.txt', 'w' )
f.write(auth)
f.close()

print('Saved Auth File')

response = requests.request("PUT", url, data=payload, headers=headers, verify=False)

 
print(response.text)
