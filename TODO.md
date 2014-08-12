x load search query results using the sqlalchemy model
x plot commit_stats available from github.

x extractor for weekly contributions from a repo.
x avoid the search results limits problems

x explore why there were duplicates in the database
x modify scripts to avoid duplicates

x removed duplicates from Repos and weeks

x explore a temporal feature maker
x explore a target maker

x build feature makers
x build something that grabs a single repo and predicts its near future.

x import flask stuff to this repo
x mvp

# analysis

- check that the EWMA code is doing the right thing. Diversity seems too big.
- implement a learning curve visualizer
- clean up feature-making tests
- see if gaps can be reincorporated, replacing nans with zeros.
- explore gap time distribution to discuss live/dead cutoff

x code to make new features
x write to Xavier
x plot exploratory data vs. target
x get cross-validation working
x play with scaling explanatory variables
x build a framework for experimentation around a scikit pipeline
x first-pass optimize logistic Regression
x try random forests and/or SVM.

# deployment

x propagated feature-making/training changes up to the website.

# improve the data story

- find concrete compelling use case example
	(what was the vega/vincent alternative?)
- continue download of Python weekly data
- clean up downloading code

x download Python repos
x download Python weekly data
- get Python weekly stragglers


# user experience

x build a short term github repo data cache module
x make website grab from cache if available
x make website load from json
- extend website to more than one 
x json data api endpoint
x bootstrap the landing page
x bootstrap the results page
- go over my old d3 practice
- add graph


Notes from talking to Div and Brandon:

the parameters to tune in a RandomForest are:
- max_features (mostly)
- n_estimators (a little)

the parameters to tune in a grandient boosting classifier:
- max_depth (key)

brandon also pointed me to his repo in which he has
encapsulated some of these workflows for reuse:

https://github.com/brandonckelly/bck_stats
note especially
bck_stats/sklearn_estimator_suite.py
