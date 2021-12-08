import json
import unittest
import os
import requests
from requests import api
import re



# pf = Petfinder(key="eKmHUqczFwsEYpfDBRo4UY3IXfkq3sL8kpWH7PohKY2UbNDd2P", secret="EqBhbmXTTd95OAohkgdTQrl0wwTP2kZMIfpkjBKO")
# dogs = pf.animal_types('dog')
apiKey="eKmHUqczFwsEYpfDBRo4UY3IXfkq3sL8kpWH7PohKY2UbNDd2P"
secret="EqBhbmXTTd95OAohkgdTQrl0wwTP2kZMIfpkjBKO"
data = {
  'grant_type': 'client_credentials',
  'client_id': "eKmHUqczFwsEYpfDBRo4UY3IXfkq3sL8kpWH7PohKY2UbNDd2P",
  'client_secret': "EqBhbmXTTd95OAohkgdTQrl0wwTP2kZMIfpkjBKO"
}
response = requests.post('https://api.petfinder.com/v2/oauth2/token', data=data)

print("PLEASE")
# print(response)
# print(response.text)
# token_code=(response.text)
token_dict=response.json()
print(token_dict['access_token'])
token_code=str(token_dict['access_token'])

# expression_full = r'(access_token\":\".+\")'
# match=re.findall(expression_full, token_code)
# token_code = match[0][15:-1]

print("HERE")
# print(token_code)

headers = {
    'Authorization': 'Bearer '+ token_code,
}

params = (
    ('limit', '40'),
    ('location', 'Detroit, MI'),
    ('distance', '10')

)

dog_data = requests.get('https://api.petfinder.com/v2/animals?type=dog&', headers=headers, params=params)
# print(animal_data)
# print(type(dog_data))
dog_dict=dog_data.json()
dog_dict=json.dumps(dog_dict)
dog_dict=json.loads(dog_dict)
print(type(dog_dict))
print(dog_dict)



# getting primary dog breed and putting in dictionary
dog_breed_count = {}
i = 0
print("UWU")
dog_dict=dog_dict["animals"]
for dog in dog_dict:
    dog_breeds=dog_dict[i]["breeds"]
    i=i+1
    main_breed = dog_breeds['primary']
    if main_breed in dog_breed_count:
        dog_breed_count[main_breed] = dog_breed_count[main_breed] + 1
    else:
        dog_breed_count[main_breed] = 1
print(dog_breed_count)
print("done")
