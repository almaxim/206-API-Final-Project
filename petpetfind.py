import json
import unittest
import os
import requests
from requests import api
import re
import sqlite3
import matplotlib.pyplot as plt
import random



def getBreeds(cur):
    a = random.randint(1,10)
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
    # token_code=(response.text)
    token_dict=response.json()
    token_code=str(token_dict['access_token'])

    # expression_full = r'(access_token\":\".+\")'
    # match=re.findall(expression_full, token_code)
    # token_code = match[0][15:-1]

    headers = {
        'Authorization': 'Bearer '+ token_code,
    }

    params = (
        ('limit', '25'),
        ('location', 'Detroit, MI'),
        ('distance', '100'),
        ('page', a)

    )

    dog_data = requests.get('https://api.petfinder.com/v2/animals?type=dog&', headers=headers, params=params)
    dog_dict=dog_data.json()
    dog_dict=json.dumps(dog_dict)
    dog_dict=json.loads(dog_dict)
    return dog_dict

def setUp_breed(dog_dict, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS breed_dog (id INTEGER PRIMARY KEY, name TEXT, gender TEXT, age TEXT, main_breed TEXT)")
    count = 1
    dog_dict=dog_dict["animals"]

    for x in dog_dict:
        id = x['id']
        name = x['name']
        gender = x['gender']
        age = x['age']
        main_breed=x['breeds']['primary']
        cur.execute("INSERT OR IGNORE INTO breed_dog (id, name, gender, age, main_breed) VALUES(?,?,?,?,?)", (id, name, gender, age, main_breed))
        count +=1
    conn.commit()

def breed_dict(dog_dict):
    # getting primary dog breed and putting in dictionary
    dog_breed_count = {}
    i = 0
    dog_dict=dog_dict["animals"]
    for dog in dog_dict:
        dog_breeds=dog_dict[i]["breeds"]
        i=i+1
        main_breed = dog_breeds['primary']
        if main_breed in dog_breed_count:
            dog_breed_count[main_breed] = dog_breed_count[main_breed] + 1
        else:
            dog_breed_count[main_breed] = 1
    return dog_breed_count


def main():
    path=os.path.dirname(os.path.abspath(__file__))
    conn=sqlite3.connect(path+'/doggo.db')
    cur=conn.cursor()
    x = getBreeds(cur) 
    setUp_breed(x, cur, conn)
    breed_dict(x)
    conn.close()
   


if __name__ == "__main__":
    main()