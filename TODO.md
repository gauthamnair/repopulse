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

analysis
x code to make new features
x write to Xavier
- plot exploratory data vs. target
- get cross-validation working
- play with scaling explanatory variables
- build a framework for experimentation around a scikit pipeline
- implement a learning curve visualizer
- first-pass optimize logistic Regression
- try random forests and/or SVM.
- clean up feature-making tests

improve the data story
- find concrete compelling use case example
	(what was the vega/vincent alternative?)
x download Python repos
- clean up downloading code
- download Python weekly data

user experience

- build a short term github repo data cache module
- make website grab from cache if available
- extend website to more than one 
- bootstrap the website to make it look nice
- go over my old d3 practice
- add graph
