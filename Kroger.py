import matplotlib.pyplot as plt
import json
import requests 
import sqlite3
import unittest
import os
import random


#Kroger API accessing up to 25 ingredients 
#https://developer.kroger.com/reference/#tag/Products 

#access API and collect 25 items of a product type randomly chosen from a list of categories
def get_kroger_data(product, offset):
    prod_type = random.choice(product)
    token = 'berrygooddata-868c67c91a28e98a3da56292fb4b55b9240571366980511557csVqVrlMIPBTjajt7w5LglfimtncmvG8V8wqmbw-'
    param = {'limit':25,'offset': offset, 'access_token':token}
    item_info = []

    #request the products of the types included
    response = requests.get(prod_type, params = param)
    all_results = response.json()
    for x in all_results:
        name = x['data']['description']
        price_reg = x['data']['items']['price']['regular']
        price_nat = x['data']['items']['nationalPrice']['regular']
        productID = x['data']['productId']
        brand = x['data']['brand']
        category= x['data']['categories']
        item_info.append((productID, name, brand, category, price_reg, price_nat))

    return item_info

def setUpDB(db_filename):
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    return cur, conn

def setUpProducts():

    pass



def main():
    unittest.main(verbosity=2)


if __name__ == "__main__":
    main()