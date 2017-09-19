import pickle, sys, requests
from lib import cleaner, query_db, response_json
from redis import Redis

if len(sys.argv) > 1:
    search_url = sys.argv[1]
    search_term = search_url.split("/")[-1]
else:
    raise IOError("Please enter a URL")

filename = 'model.sav'

REDIS = Redis('this_redis')
model_pkl = REDIS.get('model')
loaded_model = pickle.loads(model_pkl)

#loaded_model = pickle.load(open(filename, 'rb'))

url = "https://en.wikipedia.org/w/api.php"
params = {
		"action":"query",
		"prop":"extracts",
		"exlimit":"max",
		"format":"json",
		"explaintext":True,
		"titles": search_term
		}
response = response_json(url, params)
pageid = [key for key in response['query']['pages']][0]

if pageid == '-1':
	raise IOError("Please enter a valid URL, {} is not a valid URL".format(search_url))

pagetext = response['query']['pages'][pageid]['extract'].replace("'","")
pagetext = cleaner(pagetext)
cat_title = query_db("""
		            SELECT title FROM category 
		            WHERE categoryid = '{}';
		            """.format(loaded_model.predict([pagetext])[0]), fetch_res=True)

print("Recommended Wikipedia category: {}; probability = {}%"
	.format(cat_title[0]['title'].strip(), round(max(loaded_model.predict_proba([pagetext])[0]*100), 2)))
