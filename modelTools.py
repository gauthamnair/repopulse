import numpy as np
import sklearn.cross_validation
import sklearn.metrics
import pandas as pd

def addAliveOrDeadColumn(df):
	df['aliveOrDead'] = np.where(df['futureCommits_num'] > 0,
                                 'alive',
                                 'dead')

def makeTarget(df):
	return np.where(df['aliveOrDead']=='alive',1,0)

# there are nans in the gaps for items that don't have any gaps
# byRepo[colNames].apply(lambda x: np.any(np.isnan(x.values)))

_predColumns = ['daysSinceFirstCommit',
  'daysSinceLastCommit',
  # 'diversity_ewmaOneMonth',
  # 'diversity_ewmaOneYear',
  # 'diversity_ewmaSixMonth',
  # 'diversity_ewmaThreeMonth',
  # 'diversity_ewmaTwoWeeks',
  # 'diversity_pastCommits_num',
  # 'ewmaOneMonth',
  # 'ewmaOneYear',
  # 'ewmaSixMonth',
  # 'ewmaThreeMonth',
  # 'ewmaTwoWeeks',
  'adjustedOneMonth',
  'adjustedOneYear',
  'adjustedSixMonth',
  'adjustedThreeMonth',
  'adjustedTwoWeeks',
  'pastCommits_num']

# _predColumns = ['daysSinceLastCommit']


class SinglePredictor:
	def __init__(self, colName, transformer=None):
		self.colName = colName
		self.transformer = transformer

	def makePredictor(self, featuresByRepo):
		if self.transformer != None:
			return self.transformer(featuresByRepo[self.colName])
		else:
			return featuresByRepo[self.colName]

class PredictorsMaker:
	def __init__(self):
		self.singlePredictors = dict()
		self.interactions = []

	def includeColumn(self, colName, alias=None, transformer=None):
		sp = SinglePredictor(colName=colName, transformer=transformer)
		if alias == None:
			alias = colName
		self.singlePredictors[alias] = sp

	def includeInteraction(self, alias1, alias2):
		self.interactions.append((alias1, alias2))

	def makePredictors(self, featuresByRepo):
		result = dict()
		for alias, singlePredictor in self.singlePredictors.items():
			result[alias] = singlePredictor.makePredictor(featuresByRepo)

		for (alias1, alias2) in self.interactions:
			interactionAlias = alias1 + '*' + alias2
			result[interactionAlias] = result[alias1] * result[alias2]

		result = pd.DataFrame(result)
		predictorNames = list(result.keys())
		return (result.values, predictorNames)



def makePredictors(byRepo, predColumns = _predColumns):
	dfX = byRepo[predColumns]
	return (dfX.values, predColumns)


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
		return sklearn.metrics.classification_report(
			y_true=self.y_true, 
			y_pred=self.y_pred)

	def roc(self):
		(fpr, tpr, _) = sklearn.metrics.roc_curve(self.y_true, self.predScores)
		return (fpr, tpr)

	def auc(self):
		(fpr, tpr) = self.roc()
		return sklearn.metrics.auc(fpr, tpr)


def makeModelEvaluator(X, y):

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

	return evaluateModel