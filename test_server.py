import requests

url = "http://127.0.0.1:5000/"
r = requests.get(url)
print r.content

url = "http://127.0.0.1:5000/feed"

for n in range(20):
    args = {"x":n, "y":n**2, "target":"z"}
    r = requests.post(url, json=args)
    print r.content
