# Semantic Search

## The Task

The task has three parts -- data collection, data exploration / algorithm development, then finally predictive modeling. 

![](http://interactive.blockdiag.com/image?compression=deflate&encoding=base64&src=eJxdjrsOwjAMRXe-wlsmRhaQkDoiMSDxBW5slahtHDmGCiH-nfQxtKy-59zruhPfUsAGPjsA56XvMdIRSIbYCZKD_RncENqQuGBQ3S7TidCwxsynjZUZ1T8m4HqvJlXZnhrBJMHBbWlTDHEeSFravYUXQy_E3TKrwbioMKb5z16UmRxfXZurVY_GjegbhqJIjaXm-wNmzE4W)

### Part 1 -- Collection

We want you to query the wikipedia API and **collect all of the articles** under the following wikipedia categories:

* [Machine Learning](https://en.wikipedia.org/wiki/Category:Machine_learning)
* [Business Software](https://en.wikipedia.org/wiki/Category:Business_software)

We want your code to be modular enough that any valid category from Wikipedia can be queried by your code.

The results of the query should be written to PostgreSQL tables, `page` and `category`. You will also need to build some sort of reference between the pages and categories. Keep in mind that a page can have many categories and a category can have many pages so a straight foreign key arrangement will not work. 

**optional**  
Make it so that your code can be run via a python script e.g.

```bash
$ docker run -v `pwd`:/src python -m download #SOME_CATEGORY#
```

**optional**  
Make it so that your code can query nested sub-categories e.g.

```bash
$ docker run -v `pwd`:/src python -m download #SOME_CATEGORY# #NESTING_LEVEL#
```

### Part 2 -- Search

Use Latent Semantic Analysis to search your pages. Given a search query, find the top 5 related articles to the search query.

**optional**  
Make it so that your code can be run via a python script e.g.

```bash
$ docker run -v `pwd`:/src python -m search #SOME_TERM#
```

### Part 3 -- Predictive Model

In this part, we want you to build a predictive model from the data you've just indexed. Specifically, when a new article from wikipedia comes along, we would like to be able to predict what category the article should fall into. We expect a training script of some sort that is runnable and will estimate a model. 

**optional**  
Make it so that your code can be run via a python script e.g.

```bash
$ docker run -v `pwd`:/src python -m train
```

Finally, you should be able to pass the url of a wikipedia page and it will generate a prediction for the best category for that page, along with a probability of that being the correct category. 

**optional**  
Make it so that your code can be run via a python script e.g.

```bash
$ docker run -v `pwd`:/src python -m predict #URL#
```

## Infrastructure

You may use the include `docker-compose.yml` file to build your project.



