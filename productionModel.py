import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import classification_report
from sklearn.externals import joblib


def makePredictors(byRepo):
	dfX = byRepo[['daysSinceLastCommit', 'pastCommits_num', 'daysSinceFirstCommit']]
	x = dfX.values
	predictors = x[:,[0]]
	return predictors

def learnModel():
	byRepo = pd.read_csv('data/intermediate/byRepo.csv')
	del byRepo['Unnamed: 0']

	byRepo['aliveOrDead'] = np.where(byRepo['futureCommits_num'] > 0,
	                                 'alive',
	                                 'dead')

	predictors = makePredictors(byRepo)

	y = np.where(byRepo['aliveOrDead']=='alive',1,0)

	learner = linear_model.LogisticRegression()

	learner.fit(predictors, y)

	predictions = learner.predict(predictors)

	print classification_report(y_true=y, y_pred=predictions)
	joblib.dump(learner, 'productionModel.pkl')


def loadModel():
	learner = joblib.load('productionModel.pkl')
	return learner


if __name__ == '__main__':
	learnModel()

