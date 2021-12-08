import json
import unittest
import os
import requests
from requests import api
from requests.auth import HTTPBasicAuth



# pf = Petfinder(key="eKmHUqczFwsEYpfDBRo4UY3IXfkq3sL8kpWH7PohKY2UbNDd2P", secret="EqBhbmXTTd95OAohkgdTQrl0wwTP2kZMIfpkjBKO")
# dogs = pf.animal_types('dog')
apiKey="eKmHUqczFwsEYpfDBRo4UY3IXfkq3sL8kpWH7PohKY2UbNDd2P"
secret="EqBhbmXTTd95OAohkgdTQrl0wwTP2kZMIfpkjBKO"
api_url ="https://api.petfinder.com/v2/{CATEGORY}/{ACTION}?{parameter_1}={value_1}&{parameter_2}={value_2}"
fill_url = "https://api.petfinder.com/v2/animals?type=dog&page=2"
# response = requests.get(fill_url)
# response.json()
data = "grant_type=client_credentials&client_id=eKmHUqczFwsEYpfDBRo4UY3IXfkq3sL8kpWH7PohKY2UbNDd2P&client_secret=EqBhbmXTTd95OAohkgdTQrl0wwTP2kZMIfpkjBKO"
token_url="https://api.petfinder.com/v2/oauth2/token"
r =requests.post(token_url, data=data)
print(r)



headers = {'Authorization': 'Bearer eKmHUqczFwsEYpfDBRo4UY3IXfkq3sL8kpWH7PohKY2UbNDd2P'}
# auth=HTTPBasicAuth('eKmHUqczFwsEYpfDBRo4UY3IXfkq3sL8kpWH7PohKY2UbNDd2P', 'EqBhbmXTTd95OAohkgdTQrl0wwTP2kZMIfpkjBKO')



rsp = requests.get(fill_url, headers=headers)
# rsp.json()
print("DEATH")
print(rsp)
print("Done")


