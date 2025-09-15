import requests
import json
import os

f = open("modelname.txt", "r")
x = ""

for line in f:
  stripped_line = line.rstrip()
  x += stripped_line
f.close()

rasa_username = os.getenv('RASA_USERNAME')
rasa_password = os.getenv('RASA_PASSWORD')
rasa_url = os.getenv('RASA_SERVER_URL', 'https://<rasa-x route>/api/auth')

if not rasa_username or not rasa_password:
    raise ValueError("RASA_USERNAME and RASA_PASSWORD environment variables must be set")

headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache'}
payload = json.dumps({"username": rasa_username, "password": rasa_password})

r = requests.post(rasa_url, data=payload, headers=headers, verify=True)
binary = r.content
output = json.loads(binary)
auth = output['access_token']
print(auth)

url = "https://<rasa-x route>/api/projects/default/models/" + x + "/tags/production"

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

response = requests.request("PUT", url, data=payload, headers=headers, verify=True)

 
print(response.text)
