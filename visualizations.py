import json
import sqlite3
import os
import requests
from requests import api

def main():

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/doggo.db')
    cur = conn.cursor()

    conn.close()


if __name__ == "__main__":
    main()