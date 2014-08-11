import pandas as pd
import numpy as np
from sklearn import linear_model
import sklearn.cross_validation
import sklearn.metrics
from sklearn.metrics import classification_report

# there are nans in the gaps for items that don't have any gaps
# byRepo[colNames].apply(lambda x: np.any(np.isnan(x.values)))
notPredictors = ['repo_full_name', 'futureCommits_num', 'aliveOrDead']
def isAPredictor(colName):

	if (colName in notPredictors) or colName.startswith('gaps'):
		return False
	else:
		return True

def makePredictors(byRepo):
	allColumns = byRepo.keys()
	predColumns = [x for x in allColumns if isAPredictor(x)]
	dfX = byRepo[predColumns]
	return (dfX.values, predColumns)

byRepo = pd.read_csv('data/intermediate/byRepo.csv')
del byRepo['Unnamed: 0']

byRepo['aliveOrDead'] = np.where(byRepo['futureCommits_num'] > 0,
                                 'alive',
                                 'dead')

(X, colNames) = makePredictors(byRepo)
y = np.where(byRepo['aliveOrDead']=='alive',1,0)

class EvaluationReport:
	def __init__(self):
		self.y_pred = np.array([])
		self.y_true = np.array([])
		self.predScores = np.array([])

	def addTestData(self, fittedLearner, X_test, y_test):
		predScore = fittedLearner.predict_proba(X_test)[:,1]
		yhat_test = fittedLearner.predict(X_test)
		self.y_pred = np.concatenate((self.y_pred, yhat_test))
		self.y_true = np.concatenate((self.y_true, y_test))
		self.predScores = np.concatenate((self.predScores, predScore))

	def classification_report(self):
		return classification_report(
			y_true=self.y_true, 
			y_pred=self.y_pred)

	def auc(self):
		(fpr, tpr, _) = sklearn.metrics.roc_curve(self.y_true, self.predScores)
		return sklearn.metrics.auc(fpr, tpr)

def evaluateModel(learner):
	evaluationReport = EvaluationReport()
	splitter = sklearn.cross_validation.KFold(n=len(X),
		n_folds=10, shuffle=True, random_state=40)
	for train_index, test_index in splitter:
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = y[train_index], y[test_index]

		learner.fit(X_train, y_train)
		evaluationReport.addTestData(learner, X_test, y_test)
	return evaluationReport

report = evaluateModel(learner = linear_model.LogisticRegression())
