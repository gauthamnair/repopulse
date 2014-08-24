import trainingData
import productionModel
import modelTools
import numpy as np


byRepo = trainingData.load()
modelTools.addAliveOrDeadColumn(byRepo)

X, colNames = productionModel.makePredictors(byRepo)
y = modelTools.makeTarget(byRepo)

learner = productionModel.loadModel()

alive = 1
dead = 0

probAlive = learner.predict_proba(X)[:,alive]

predictedAlive = learner.predict(X)

byRepo['probAlive'] = probAlive
byRepo['predicted'] = np.where(predictedAlive == 1, 'alive', 'dead')

byRepo.to_csv('data/intermediate/byRepoWithPredictions.csv')