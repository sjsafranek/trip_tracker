import requests

url = 'http://0.0.0.0:5000'


resp = requests.post(url + '/api/v1/device')
if 200 != resp.status_code:
    raise ValueError(resp.text)

device_id = resp.json()['data']['device']['device_id']


resp = requests.post(url + '/api/v1/trip', params={'device_id': device_id, 'position': '0,0'})
print(resp.text)


for i in range(90):
    resp = requests.post(url + '/api/v1/location', params={'device_id': device_id, 'position': '{0},0'.format(i)})
    print(resp.text)



resp = requests.delete(url + '/api/v1/trip', params={'device_id': device_id, 'position': '2,0'})
print(resp.text)
