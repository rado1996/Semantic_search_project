import sys
import pandas as pd
from lib import connect_to_db, query_db, cleaner, response_json

#sys.argv = ["query.py", "Machine learning"]

cat = []
cat_nxt_lvl = []
if len(sys.argv) > 2:
    lvl = int(sys.argv[2])
elif len(sys.argv) == 2:
	lvl = 1
else:
    raise IOError("Please enter a category")

cat_nxt_lvl.append(sys.argv[1])

for levels in range(lvl):

	cat = cat_nxt_lvl
	cat_nxt_lvl = []
	if levels == 0:
		parentcategory = True
	else:
		parentcategory = False

	for category in cat:

		check_categoryid = query_db("""
		                    SELECT categoryid FROM category 
		                        WHERE title = '{}';
		                    """.format(category), fetch_res=True)

		if len(check_categoryid) == 0:
		    query_db("""
		            BEGIN;
		            INSERT INTO category (title, parentcategory)
		                VALUES ('{}', {});
		            COMMIT;
		            """.format(category, parentcategory), fetch_res=False)


		categoryid = query_db("""
		                    SELECT categoryid FROM category 
		                        WHERE title = '{}';
		                    """.format(category), fetch_res=True)

		    
		url = "https://en.wikipedia.org/w/api.php"
		params = {
		    	"action":"query",
		    	"list":"categorymembers",
		    	"cmlimit":"max",
		    	"format":"json",
		    	"cmtitle":"Category:" + category
				}

		response = response_json(url, params)

		num_docs = len([entry['title'] for entry in response['query']['categorymembers'] if entry['title'][:9] != 'Category:'])
		print("Downloading {} {} pages".format(str(num_docs), category))

		for entry in response['query']['categorymembers']:

			pageid = entry["pageid"]
			title = entry["title"].replace("'","")
			if title[:9] != "Category:":

				check_pageid = query_db("""
		                        SELECT pageid FROM page 
		                            WHERE pageid = {};
		                        """.format(str(pageid)), fetch_res=True)

				if len(check_pageid) == 0:
					url = "https://en.wikipedia.org/w/api.php"
					params = {
			                "action":"query",
			                "prop":"extracts",
			                "exlimit":"max",
			                "format":"json",
			                "explaintext":True,
			                "pageids": str(pageid)
			                }

					response = response_json(url, params)
					pagetext = response['query']['pages'][str(pageid)]['extract'].replace("'","")
					pagetext = cleaner(pagetext)
		        
					query_db("""
		                    BEGIN;
		                    INSERT INTO page (pageid, title, pagetext)
		                        VALUES ({}, '{}', '{}');
		                    COMMIT;
		                    """.format(str(pageid), title, pagetext), fetch_res=False)

					query_db("""
		                    BEGIN;
		                    INSERT INTO page_category (pageid, categoryid)
		                        VALUES ({}, {});
		                    COMMIT;
		                    """.format(pageid, categoryid[0]['categoryid']), fetch_res=False)
			else:
				cat_nxt_lvl.append(title.replace("Category:",""))

		   