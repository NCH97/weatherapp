import web
import json
import requests
import sqlite3
from sqlite3 import Error
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('PROJECT_API_KEY')



urls = (
    '/weather','Temp'
)

app = web.application(urls,globals())

#Creation database

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        sql = '''CREATE TABLE temperature (
                         id INTEGER PRIMARY KEY,
                         zip_code INTEGER NOT NULL,
                         TEMP FLOAT NOT NULL,
                         TEMP_MIN FLOAT NOT NULL,
                         TEMP_MAX FLOAT NOT NULL
                  );'''
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

#Creation table
def create_table(db_file):
    try:
        conn = sqlite3.connect(db_file)
        sql = '''CREATE TABLE temperature (
                                 id INTEGER PRIMARY KEY,
                                 zip_code INTEGER NOT NULL,
                                 TEMP FLOAT NOT NULL,
                                 TEMP_MIN FLOAT NOT NULL,
                                 TEMP_MAX FLOAT NOT NULL
                          );'''
        cur = conn.cursor()
        print("Connexion réussie à SQLite")
        cur.execute(sql)
        conn.commit()
        print("Table SQLite est créée")
        cur.close()
        conn.close()
        print("Connexion SQLite est fermée")
    except sqlite3.Error as error:
        print("Erreur lors de la création du table SQLite", error)

#insertion data
def insertdata(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        print("Connexion réussie à SQLite")
        sql = "INSERT INTO temperature (zip_code,TEMP,TEMP_MIN,TEMP_MAX) VALUES (37000,12.0,7.0,15.0)"
        count = cur.execute(sql)
        conn.commit()
        print("Enregistrement inséré avec succès dans la table")
        cur.close()
        conn.close()
        print("Connexion SQLite est fermée")
    except sqlite3.Error as error:
        print("Erreur lors de l'insertion dans la table", error)

class Temp:
    def GET(self):
        web.headers = {"content-type":"application/json"}
        zip = str(web.input().zipcode)
        url_w = f"http://api.openweathermap.org/data/2.5/weather?zip={zip},fr&appid={API_KEY}"

        r_weather = requests.get(url_w)
        data = r_weather.json()
        t = data['main']['temp']
        t_min = data['main']['temp_min']
        t_max = data['main']['temp_max']
        météo = data['weather'][0]['description']

        jsonResponse = json.dumps({
            "City": {
                "Temperature": t-273.15,
                "Temperature_min": t_min-273.15,
                "Temperature_max": t_max - 273.15,
                "Meteo": météo
            }
        })
        return  (jsonResponse)

if __name__ == '__main__':
    app.run()