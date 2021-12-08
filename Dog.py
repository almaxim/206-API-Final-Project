import json
import sqlite3
import os
import requests
from requests import api
import csv
import matplotlib.pyplot as plt



def getDogs(offset, cur):
    api_key = "251783e2-365b-42fd-8c8d-12dc9e298266"
    headers = { 
        "x-api-key" : api_key
    }
    param = {'limit':25, 'offset': offset}

    breed_check = r"https://api.thedogapi.com/v1/breeds"
    page = requests.get(breed_check, params= param)
    data = json.loads(page.text)
    return data

def setUp(data, off, cur, conn): 
    cur.execute("CREATE TABLE IF NOT EXISTS Dog_Breeds (id INTEGER PRIMARY KEY, name TEXT, temperament TEXT, life_span TEXT, origin TEXT, weight DOUBLE)")

    count = 1
    for x in data: 
        id = off + count
        name = x['name']
        temp = x['temperament']
        life = x['life_span']
        origin = x['origin']
        weight = x['weight']
        cur.execute("INSERT OR IGNORE INTO Dog_Breeds (id, name, temperament, life_span, origin, weight) VALUES(?,?,?,?,?,?)", (id, name, temp, life, origin, weight))
        count += 1

    conn.commit()

def main():
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/doggo.db')
    cur = conn.cursor()

    try: 
        cur.execute('SELECT id FROM Dog_Breeds WHERE id = (SELECT MAX(id) FROM Dog_Breeds)')
        start = cur.fetchone()
        off = start[0]
    except: 
        off = 0

    x = getDogs(off, cur) 
    setUp(x, off, cur, conn)

    conn.close()


if __name__ == "__main__":
    main()