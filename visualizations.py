import json
import sqlite3
import os
import requests
from requests import api
import petpetfind
import Dog
import csv
import matplotlib.pyplot as plt
import numpy as np
import random

def most_common_temperament(cur,conn):
    cur.execute("""
    SELECT COUNT(*), temperament_type
    FROM Dog_Breeds
    INNER JOIN breed_dog
    ON breed_dog.main_breed = Dog_Breeds.name
    INNER JOIN Dog_Temperaments
    ON Dog_Temperaments.temperanent_id=Dog_Breeds.temperament
    GROUP BY Dog_Temperaments.temperament_type
    """)
    return cur.fetchall()

def most_common_temperament_vers1(cur,conn):
    cur.execute("""
    SELECT COUNT(*), temperament
    FROM Dog_Breeds
    JOIN breed_dog
    ON breed_dog.main_breed = Dog_Breeds.name
    GROUP BY Dog_Breeds.temperament
    """)
    return cur.fetchall()

def viz_one(data):
    color_list=[]
    temperament_type = []
    number = []
    for i in data:
        temperament_type.append(i[1])
        number.append(i[0])
        r = random.random()
        b = random.random()
        g = random.random()
        c = (r, g, b)
        color_list.append(c)
    plt.bar(temperament_type, number, color = color_list)
    plt.xticks(rotation=90)
    plt.xlabel('Temperament Type')
    plt.ylabel('Number of Dogs')
    plt.title("Number of Dogs for Temperament Type")
    plt.show()

#Create pie chart using averages for each temperament type
def viz_two(data, lists, temp_name):
    temps = []
    percents = []
    color_list=[]
    for i in data: 
        id = int(i[1])
        name = temp_name.get(id)
        temps.append(name)
        r = random.random()
        b = random.random()
        g = random.random()
        c = (r, g, b)
        color_list.append(c)
    for x in lists: 
        percents.append(x)

    mylabels = temps
    mycolors = ['red', 'pink', 'orange', 'yellow', 'green','blue', 'navy', 'indigo', 'purple', 'violet', 'black', 'grey']

    plt.pie(percents,labels = mylabels, colors = color_list, shadow=True, startangle=90, textprops={'fontsize': 8})
    plt.axis('equal')
    plt.title("Average Percent of Dogs for Adoption in a Group with a Temperament", pad = 15)
    plt.show()


def main():

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/doggo.db')
    cur = conn.cursor()
    


    x=petpetfind.getBreeds(cur)
    petpetfind.setUp_breed(x, cur, conn)
    petpetfind.breed_dict(x)

    try: 
        cur.execute('SELECT id FROM Dog_Breeds WHERE id = (SELECT MAX(id) FROM Dog_Breeds)')
        start = cur.fetchone()
        off = start[0]
    except: 
        off = 0

    x = Dog.getDogs(off, cur) 
    Dog.setUpTemp(x, cur, conn)
    Dog.setUpBreeds(x, cur, conn)

    combine_table='SELECT breed_dog.id, breed_dog.name, breed_dog.gender, breed_dog.age,  Dog_Breeds.name, Dog_Breeds.temperament, Dog_Breeds.life_span, Dog_Breeds.weight FROM breed_dog INNER JOIN Dog_Breeds on breed_dog.main_breed=Dog_Breeds.name'
    cur.execute(combine_table)  
    #Makes list of all dogs in breed_dog with breed, id, gender, temperament, etc.
    myresult = cur.fetchall()

    #dictionary of dog temperament id and temperament name
    cur.execute('SELECT temperanent_id,temperament_type FROM Dog_Temperaments')
    names = cur.fetchall()
    temperament_name = {}
    for x in names:
        temperament_name[x[0]] = x[1]

    
    #find average of each temperament from total
    temp_list = []
    #dictionary with temp and times it appears
    temp_count = {}
    avg_list = []

    for t in myresult: 
        val = int(t[5])

        if val not in temp_list: 
            temp_list.append(val)
            temp_count[val] = 1
        else: 
            temp_count[val] = temp_count.get(val) + 1

    for x in temp_list:
        avg_list.append(temp_count.get(x) / len(myresult))

    vals = zip(temp_list, avg_list)
    data = list(vals)
    dir = os.path.dirname('DogTemperaments.txt')
    out_file = open(os.path.join(dir, 'DogTemperaments.txt'), "w")
    with open('DogTemperaments.txt') as f:
        csv_writer = csv.writer(out_file, delimiter=",", quotechar='"')
        csv_writer.writerow(["Temperament Id","Percent of Dogs in a Group with that Temperament"])
        for y in data:
            csv_writer.writerow([y[0], y[1]])


    combine_data=most_common_temperament(cur,conn)
    combine_data_1=most_common_temperament_vers1(cur,conn)
    viz_one(combine_data)
    viz_two(combine_data_1, avg_list, temperament_name)
    conn.close()



if __name__ == "__main__":
    main()