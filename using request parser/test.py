import requests

URL = 'http://127.0.0.1:5000/'
# To get a single request
response = requests.get(URL + '/video/1')
print(response.json())

# To add a request
response = requests.post(URL + 'video',
                         {'name': 'Natural Language Processing', 'views': 1688710, 'likes': 10340})
print(response.json())

response = requests.get(URL + 'videos')
print(response.json())

# To delete a specific request
response = requests.delete(URL + '/video/4')
print(response)

response = requests.get(URL + '/video')
print(response.json())
