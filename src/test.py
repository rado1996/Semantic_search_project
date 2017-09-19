import pandas as pd
from lib import connect_to_db, query_db, cleaner

text = "hello world jkldsjfd"

print(cleaner(text))