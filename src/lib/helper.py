import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import re
from spacy.en import STOP_WORDS
from spacy.en import English
import requests

def connect_to_db():
    con = pg2.connect(host='postgres',
                      dbname='postgres',
                      user='postgres')
    cur = con.cursor(cursor_factory=RealDictCursor)
    return con, cur

def query_db(query, fetch_res=True):
    con, cur = connect_to_db()
    cur.execute(query)
    if fetch_res:
        results = cur.fetchall()
    else:
        results = None
    con.close()
    return results

def cleaner(text):
    nlp = English()
    text = re.sub('<.>', ' ', text)
    text = re.sub('<..>', ' ', text)
    text = re.sub('\.+', ' ', text)
    text = re.sub('[^a-z0-9 ]','', text.lower())
    text = re.sub('\d+','NUMBER ',text)
    text = re.sub('\s+',' ',text)
    text = ' '.join(i.orth_ for i in nlp(text) if i.orth_ not in STOP_WORDS)
    return text

def response_json(url, params):
    response = requests.get(url, params = params)
    return response.json()