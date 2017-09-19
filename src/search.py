from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
import numpy as np
import sys
from lib import connect_to_db, query_db, cleaner

#sys.argv = ["search.py", "Machine learning"]

if len(sys.argv) > 2:
    search_term = sys.argv[1]
    matches = int(sys.argv[2])
elif len(sys.argv) == 2:
    search_term = cleaner(sys.argv[1])
    matches = 5
else:
    raise IOError("Please enter a search term")

pages = query_db("""
                SELECT * FROM page;
                """, fetch_res=True)

page_ids = [page['pageid'] for page in pages]
page_titles = [page['title'] for page in pages]
page_texts = [page['pagetext'] for page in pages]
page_texts.append(search_term)
doc_idx = len(page_ids)

vec = CountVectorizer(min_df = 1, stop_words='english')
vec_fit = vec.fit_transform(page_texts)

svd = TruncatedSVD(300, algorithm= 'randomized')
norm = Normalizer(copy=False)
pipe = make_pipeline(svd, norm)
lsa = pipe.fit_transform(vec_fit)

sim_mat = np.asarray(np.asmatrix(lsa) * np.asmatrix(lsa).T)

sim_mat_idx = np.column_stack((sim_mat,np.arange(len(sim_mat)))) 
sim_mat_idx = sim_mat_idx[sim_mat_idx[:, doc_idx].argsort()[::-1]]
sim_mat_idx = sim_mat_idx[:,len(sim_mat)].astype(int)

print("Top {} articles related to {}:".format(matches, search_term))
for i in range(matches):
    pg_index = sim_mat_idx[i+1]
    print(page_ids[pg_index], page_titles[pg_index])

