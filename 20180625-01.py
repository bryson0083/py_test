import requests

url = "https://notify-api.line.me/api/notify"  
token = 'xvuBkzVt5cmEbcYVztU4nluEpB69eAP7j1QeXJWiq3z'
headers = {"Authorization" : "Bearer "+ token}

message =  'test msg'
payload = {"message" :  message}
picURI = 'tb_img2.png'
files = {'imageFile': open(picURI, 'rb')}
r = requests.post(url ,headers = headers ,params=payload, files = files)
print(r)