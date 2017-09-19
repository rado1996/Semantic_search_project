from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from lib import connect_to_db, query_db
import numpy as np
import pickle
from redis import Redis

print("Retrieving page data...")

pages = query_db("""
                SELECT category.categoryid, pagetext 
                FROM page, page_category, category 
                WHERE page.pageid = page_category.pageid 
                AND category.categoryid = page_category.categoryid  
                AND category.parentcategory = True;
                """, fetch_res=True)
page_texts = [page['pagetext'] for page in pages]
category_ids = [page['categoryid'] for page in pages]

X = page_texts
y = category_ids

nlp_pipe = Pipeline([
    ('vec',TfidfVectorizer()),
    ('clf',LogisticRegression(random_state=42))
])

nlp_params = {
    'vec__ngram_range':[(1,2),(1,3)],
    'vec__min_df':[1,2],
    'clf__C':np.logspace(-2,4,7)
}

print("Running training model...")

nlp_gs = GridSearchCV(nlp_pipe, 
                      nlp_params, 
                      cv=StratifiedShuffleSplit(5, random_state=42))

nlp_gs.fit(X, y)

print("Train score: {}".format(nlp_gs.score(X, y)))

filename = 'model.sav'
#model_pkl = pickle.dump(nlp_gs, open(filename, 'wb'))
model_pkl = pickle.dumps(nlp_gs)

REDIS = Redis('this_redis')
REDIS.set('model', model_pkl)


