from sklearn import linear_model
import sklearn.preprocessing
import sklearn.pipeline
import sklearn.metrics
import sklearn.ensemble
from sklearn.externals import joblib

import trainingData
import modelTools


def makePredictors(featuresByRepo):
	return modelTools.makePredictors(featuresByRepo)


def learnModel():
	byRepo = trainingData.load()
	modelTools.addAliveOrDeadColumn(byRepo)

	(X, colNames) = makePredictors(byRepo)
	y = modelTools.makeTarget(byRepo)

	learner = sklearn.pipeline.Pipeline(
		[('scaler', sklearn.preprocessing.StandardScaler()),
		('logistic', linear_model.LogisticRegression())])

	learner.fit(X, y)
	predictions = learner.predict(X)
	print sklearn.metrics.classification_report(y_true=y, y_pred=predictions)
	joblib.dump(learner, 'persistentModel/productionModel.pkl')


def loadModel():
	learner = joblib.load('persistentModel/productionModel.pkl')
	return learner

if __name__ == '__main__':
	learnModel()

