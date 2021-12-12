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
import re

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
    SELECT COUNT(*),temperament
    FROM Dog_Breeds
    JOIN breed_dog
    ON breed_dog.main_breed = Dog_Breeds.name
    GROUP BY Dog_Breeds.temperament
    """)
    return cur.fetchall()

def most_common_size(cur, conn):
    cur.execute("""
    SELECT COUNT(*), weight
    FROM Dog_Breeds
    JOIN breed_dog
    ON breed_dog.main_breed = Dog_Breeds.name
    GROUP BY Dog_Breeds.weight
    """)
    return cur.fetchall()

def most_common_breed(cur,conn):
    cur.execute("""
    SELECT COUNT(*), Dog_Breeds.name
    FROM Dog_Breeds
    JOIN breed_dog
    ON breed_dog.main_breed = Dog_Breeds.name
    GROUP BY Dog_Breeds.name
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
    plt.tight_layout()
    plt.show()  

# Create pie chart using averages for each temperament type
def viz_two(data):
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
    
    mylabels = temperament_type
    patches, texts = plt.pie(number, colors = color_list, shadow=True, startangle=90, textprops={'fontsize': 8})
    plt.legend(patches, mylabels, loc="best")
    # plt.pie(number,labels = mylabels, colors = color_list, shadow=True, startangle=90, textprops={'fontsize': 8})
    plt.axis('equal')
    plt.title("Average Percent of Dogs for Adoption in a Group with a Temperament", pad = 15)
    plt.show()


# def viz_two(data, lists, temp_name):
#     temps = []
#     percents = []
#     color_list=[]
#     for i in data: 
#         print(data)
#         id = int(i[1])
#         name = temp_name.get(id)
#         temps.append(name)
#         r = random.random()
#         b = random.random()
#         g = random.random()
#         c = (r, g, b)
#         color_list.append(c)
#     for x in lists: 
#         percents.append(x)

#     mylabels = temps

#     plt.pie(percents,labels = mylabels, colors = color_list, shadow=True, startangle=90, textprops={'fontsize': 8})
#     plt.axis('equal')
#     plt.title("Average Percent of Dogs for Adoption in a Group with a Temperament", pad = 15)
#     plt.show()
def viz_three(data):
    i = 0
    rand_number=[]
    expression_lower = r'\S+ -'
    expression_higher = r'- \S+'
    for dog in data:
        if isinstance(data[i][1], str) == True:
            string = data[i][1]
            num_1=re.findall(expression_lower, string)
            for match in num_1:
                num_1 = float(num_1[0][0:-2])
            num_2 = re.findall(expression_higher, string)
            for match in num_2:
                num_2 = float(num_2[0][2:])
            try:
                num_3 = random.randint(num_1,num_2)
            except:
                num_3 = num_2
        else:
            num_3 = float(data[i][1])
        rand_number.append(num_3)
        i = i+1
    plt.hist(rand_number, density=False, bins=10, rwidth=0.9)  
    plt.ylabel('Number of Dogs')
    plt.xlabel('Weight Range (lbs)')
    plt.title("Number of Dogs for Adoption by Weight Range (lbs)")
    plt.show()

def viz_four(data):
    color_list=[]
    number = []
    breed=[]
    for i in data:
        breed.append(i[1])
        number.append(i[0])
        r = random.random()
        b = random.random()
        g = random.random()
        c = (r, g, b)
        color_list.append(c)
    plt.bar(breed, number, color = color_list)
    plt.xticks(rotation=90)
    plt.xlabel('Breed')
    plt.ylabel('Number of Dogs')
    plt.title("Number of Dogs For Adoption by Recognized Breeds")
    plt.tight_layout()
    plt.show()

def viz_five(data, lists): 
    percents = []
    temps = []

    for i in data: 
        id = int(i[1])
        temps.append(id)
    for x in lists: 
        percents.append(x)
    
    N = len(percents)
    colors = np.random.rand(N)

    plt.scatter(temps, percents, c=colors, alpha=0.5)
    plt.xlabel('Temperament Type (based on id order)')
    plt.ylabel('Average Percent of Dogs')
    plt.title("Average(%) of Dogs for Adoption in a Group with a Temperament")
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
    # avg_dict ={}
    for t in myresult:
        val = int(t[5])
        if val not in temp_list: 
            temp_list.append(val)
            temp_count[val] = 1
        else: 
            temp_count[val] = temp_count.get(val) + 1

    for x in temp_count:
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
    combine_data_2 = most_common_size(cur,conn)
    combine_data_3=most_common_breed(cur,conn)


    viz_one(combine_data)
    viz_two(combine_data)
    viz_three(combine_data_2)
    viz_four(combine_data_3)
    viz_five(combine_data_1, avg_list)

    conn.close()



if __name__ == "__main__":
    main()