from sklearn import linear_model
import sklearn.cross_validation
import sklearn.metrics
import sklearn.ensemble
import sklearn.preprocessing
import sklearn.pipeline
import modelTools
import trainingData

byRepo = trainingData.load()

modelTools.addAliveOrDeadColumn(byRepo)

(X, colNames) = modelTools.makePredictors(byRepo)
y = modelTools.makeTarget(byRepo)

evaluateModel = modelTools.makeModelEvaluator(X, y)

logistic = linear_model.LogisticRegression()
reportLogistic = evaluateModel(learner = logistic)

scaledLogistic = sklearn.pipeline.Pipeline(
	[('scaler', sklearn.preprocessing.StandardScaler()),
	('logistic', linear_model.LogisticRegression())]) 
reportScaledLogistic = evaluateModel(scaledLogistic)

Cvalues = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
results = []
for C in Cvalues:
	scaledLogistic.set_params(logistic__C=C)
	results.append(evaluateModel(scaledLogistic))
for c, result in zip(Cvalues, results):
	print c, ': auc=', result.auc()

reportForest = evaluateModel(learner = sklearn.ensemble.RandomForestClassifier())
print reportForest.classification_report()