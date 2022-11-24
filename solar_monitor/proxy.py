import requests


def power_details(url, username, password):
    headers = {'content-type': 'application/json'}
    response = requests.get(url, headers=headers, auth=(username, password))
    return response.status_code, response.json()
