import matplotlib.pyplot as plt
import json
import requests 
import sqlite3
import unittest
import os
import Kroger

def setUpAPI():
    #Kroger API access
    #https://developer.kroger.com/reference/#tag/Products 
    token = "berrygooddata-868c67c91a28e98a3da56292fb4b55b9240571366980511557csVqVrlMIPBTjajt7w5LglfimtncmvG8V8wqmbw-"

    #access API and create client
    token_url = 'https://api.kroger.com/v1/connect/oauth2/token'

    headers = { 'Content-Type':'application/x-www-form-urlencoded',
        'Authorization': f'Basic {"YmVycnlnb29kZGF0YS04NjhjNjdjOTFhMjhlOThhM2RhNTYyOTJmYjRiNTViOTI0MDU3MTM2Njk4MDUxMTU1N2NzVnFWcmxNSVBCVGphanQ3dzVMZ2xmaW10bmNtdkc4Vjh3cW1idy0="}',}

    payload = {
            'grant_type':"client_credentials",
            'scope':['product.compact'],
        }

    response = requests.post(token_url, headers=headers, data=payload)
    return json.loads(response.text).get('access_token')
        

def search_products(token, term, limit=25):
    #/v1/products
    add = "&filter.term=${" + term + "}"
    base_url = "https://api.kroger.com/v1/products?"
    urls = requests.get(base_url + add)

    data = (urls.json()).get('data')
    # return [Product.from_json(product) for product in data]
    return data

    # #request the products of the types included
    # response = client.search_products(term=item, limit=25)
    # # all_results = response.json()
    # for x in response:
    #     name = x['data']['description']
    #     price_reg = x['data']['items']['price']['regular']
    #     price_nat = x['data']['items']['nationalPrice']['regular']
    #     productID = x['data']['productId']
    #     brand = x['data']['brand']
    #     category= x['data']['categories']
    #     item_info.append((productID, name, brand, category, price_reg, price_nat))

    #     return item_info


def main():
    token = setUpAPI()


    val = input("Enter the product you want to find: ")
    search = search_products(token, val)
    print(search)
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/music.db')
    cur = conn.cursor()



    unittest.main(verbosity=2)


if __name__ == "__main__":
    main()