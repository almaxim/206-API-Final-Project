import json
import sqlite3
import os
import requests
from requests import api
import petpetfind
import Dog


def main():

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/doggo.db')
    cur = conn.cursor()
    x=petpetfind.getBreeds(cur)
    petpetfind.setUp_breed(x, cur, conn)
    petpetfind.breed_dict(x)
    combine_table='SELECT breed_dog.id, breed_dog.name, breed_dog.gender, breed_dog.age,  Dog_Breeds.name, Dog_Breeds.temperament, Dog_Breeds.life_span, Dog_Breeds.weight FROM breed_dog INNER JOIN Dog_Breeds on breed_dog.main_breed=Dog_Breeds.name'
    cur.execute(combine_table)
    myresult = cur.fetchall()
    for x in myresult:
        print(x)
    conn.close()


if __name__ == "__main__":
    main()