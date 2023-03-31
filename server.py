from flask import Flask, jsonify
import sqlite3 as sql
app = Flask(__name__)
import scrapper
import os
import json
from datetime import date
import schedule
import time

con = sql.connect('database.db',check_same_thread=False)
con.execute("CREATE TABLE IF NOT EXISTS articles(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,link TEXT,author TEXT type UNIQUE,datenow TEXT);")
con.close()


def get_db_connection():
    conn = sql.connect('database.db')
    conn.row_factory = sql.Row
    return conn

def Background_Script():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_data = os.path.join(SITE_ROOT, "./JSON_Data/", f"{dt}_verge.json")
    data = json.load(open(json_data))
    print("Data extracted")
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            for item in data:
                id = int(item[0])
                title = item[1]
                url = item[2]
                author = item[3]
                date = item[4]
                cur.execute("INSERT INTO articles(title,link,author,datenow) VALUES (?,?,?,?)",(title, url, author, date))
                con.commit()
            msg = "Record successfully added"
            print(msg)
    except:
        con.rollback()
        msg = "error in insert operation"
        print(msg)
    
    finally:
        con.close()

def Current_Day():
    scrapper.main()
    Background_Script()

schedule.every().day.at("18:35").do(Current_Day)

    
@app.route('/')
def home():
    Current_Day()
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM articles').fetchall()
    conn.close()
    _json=[]
    key=["id","title","link","author","datenow"]
    for i in range(len(data)):
        item={}
        ct=0
        for j in data[i]:
            item[key[ct]]=j
            ct+=1
        _json.append(item)
    # print(_json)
    return jsonify(_json)


if __name__ == '__main__':
   app.run(debug = True)