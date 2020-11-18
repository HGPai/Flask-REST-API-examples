import requests

URL = 'http://127.0.0.1:5000/'
# To get a single request

data = [{'name': 'Neural Network programming with Pytorch', 'views': 152000, 'likes': 14500},
        {'name': 'Natural Language Processing', 'views': 120300, 'likes': 12662},
        {'name': 'Python OOPs concepts', 'views': 1111020, 'likes': 10220}]

for i in range(len(data)):
    response = requests.put(URL + 'video/' + str(i), data[i])
    print(response.json())

response = requests.delete(URL + 'video/1')
print(response.json())

response = requests.get(URL + 'video/1')
print(response.json())
