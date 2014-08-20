import numpy as np
import sklearn.cross_validation
import sklearn.metrics


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