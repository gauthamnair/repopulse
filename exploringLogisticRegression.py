from sklearn import linear_model
import sklearn.cross_validation
import sklearn.metrics
import sklearn.ensemble
import sklearn.preprocessing
import sklearn.pipeline
import modelTools
import trainingData
import numpy as np
import pandas as pd

byRepo = trainingData.load()

modelTools.addAliveOrDeadColumn(byRepo)

y = modelTools.makeTarget(byRepo)

allColumns = modelTools._predColumns

print "using all predictors"

def evaluatePredictors(predColumns = allColumns):
	learner = sklearn.pipeline.Pipeline(
		[('scaler', sklearn.preprocessing.StandardScaler()),
		('logistic', linear_model.LogisticRegression())]) 

	(X, colNames) = modelTools.makePredictors(byRepo, predColumns = predColumns)

	evaluateModel = modelTools.makeModelEvaluator(X, y)
	report = evaluateModel(learner)

	print report.classification_report()
	print "auc:", report.auc()

	learner.fit(X, y)
	return (learner, colNames)


def effectOfExcludingColumns(toExclude):
	print "excluding ", toExclude, ":"
	(learner, colNames) = evaluatePredictors(predColumns=[p for p in allColumns if p not in toExclude])
	logistic = learner.named_steps['logistic']
	print pd.Series(data=np.concatenate( (logistic.coef_[0], logistic.intercept_) ), 
		index = colNames + ['intercept'])
	print "\n\n\n"


effectOfExcludingColumns([])

toExclude = ['daysSinceLastCommit']
effectOfExcludingColumns(toExclude)

toExclude = ['daysSinceLastCommit', 'ewmaTwoWeeks', 'ewmaOneMonth']
effectOfExcludingColumns(toExclude)

toExclude = ['daysSinceLastCommit'] + [x for x in allColumns if x.startswith('ewma')]
effectOfExcludingColumns(toExclude)

toExclude = ['daysSinceLastCommit', 'pastCommits_num'] + [x for x in allColumns if x.startswith('ewma')]
effectOfExcludingColumns(toExclude)

