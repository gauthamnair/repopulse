from sklearn import linear_model
import sklearn.preprocessing
import sklearn.pipeline
import sklearn.metrics
import sklearn.ensemble
from sklearn.externals import joblib

import trainingData
import modelTools


def makePredictors(featuresByRepo):
	pm = modelTools.PredictorsMaker()

	toAdd = ['daysSinceLastCommit', 'pastCommits_num', 'daysSinceFirstCommit']
	toAdd += [x for x in featuresByRepo.keys() if x.startswith('ewma')]
	toAdd += [x for x in featuresByRepo.keys() if x.startswith('diversity')]
	
	for colName in toAdd:
	    pm.includeColumn(colName)
	return pm.makePredictors(featuresByRepo)

def makeTrainedModel():
	byRepo = trainingData.load()
	modelTools.addAliveOrDeadColumn(byRepo)

	(X, colNames) = makePredictors(byRepo)
	y = modelTools.makeTarget(byRepo)

	learner = sklearn.pipeline.Pipeline(
		[('scaler', sklearn.preprocessing.StandardScaler()),
		('logistic', linear_model.LogisticRegression())])

	learner.fit(X, y)
	return (learner, X, y)

def printModelEvaluation(learner, X, y):
	predictions = learner.predict(X)
	print sklearn.metrics.classification_report(y_true=y, y_pred=predictions)

def saveModelAsProductionModel(learner):
	joblib.dump(learner, 'persistentModel/productionModel.pkl')

def loadModel():
	learner = joblib.load('persistentModel/productionModel.pkl')
	return learner

if __name__ == '__main__':
	(learner, X, y) = makeTrainedModel()
	printModelEvaluation(learner, X, y)
	saveModelAsProductionModel(learner)

