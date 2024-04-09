import requests

url = 'https://meme-api.com/gimme'

response = requests.get(url)
meme_json = response.json()
meme_url = meme_json["url"]

print(meme_url)