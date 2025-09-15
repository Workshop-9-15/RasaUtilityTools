import requests
import json

f = open("modelname.txt", "r")
x = ""

for line in f:
  stripped_line = line.rstrip()
  x += stripped_line
f.close()

# Configure the below URL with the route to your rasa-x api/auth
url = 'https://<rasa-x route>/api/auth'
headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache'}
# Configure the below payload to your rasa-x username and password
payload = '{"username": "me", "password": "rasaxpassword"}'

r = requests.post(url, data=payload, headers=headers)
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

response = requests.request("PUT", url, data=payload, headers=headers)

 
print(response.text)
