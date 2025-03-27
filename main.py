import requests

response = requests.get("https://wizard-world-api.herokuapp.com/Wizards")
if response.status_code == 200:
    data = response.json()
    for wizard in data[:5]:
        print(wizard['firstName'], wizard['lastName'])