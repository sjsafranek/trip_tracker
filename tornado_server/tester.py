import requests

url = 'http://0.0.0.0:5000'


resp = requests.post(url + '/api/v1/device')
if 200 != resp.status_code:
    raise ValueError(resp.text)

device_id = resp.json()['data']['device']['device_id']


resp = requests.post(url + '/api/v1/device/{0}/trip'.format(device_id), params={'position': '0,0'})
print(resp.text)


for i in range(10):
    resp = requests.put(url + '/api/v1/device/{0}/waypoint'.format(device_id), params={'position': '{0},0'.format(i)})
    print(resp.text)



resp = requests.delete(url + '/api/v1/device/{0}/trip'.format(device_id), params={'position': '2,0'})
print(resp.text)
