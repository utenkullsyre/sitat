import requests

# r_get = requests.get('http://127.0.0.1:5000/api/sitat')
# print(r_get.json())

r_get = requests.get('http://127.0.0.1:5000/api/hello')
print(r_get.json())

humoer = ['Sint', 'Irritert', 'Misunnelig', 'Redd', 'Glad', 'Kjempeglad', 'Illsint']

r_post = requests.post('http://127.0.0.1:5000/api/sitat', json={"sitat":"Snille pappa!", "humoer_id":"1", "barn_id":"0"})
